from __future__ import annotations

from json import dump, load
from os import getenv
from pathlib import Path
from shutil import copyfile
from time import sleep
from typing import TYPE_CHECKING, cast

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

if TYPE_CHECKING:  # cov: ignore
    from typing import Any, Dict, List, Optional, Set, Union

    from sphinx.application import Sphinx

package_json_path = Path(__file__).parent / "package.json"
if not package_json_path.exists():
    copyfile(Path(__file__).parent.parent / "jssrc" / "package.json", package_json_path)
    for _ in range(10):
        if package_json_path.exists():
            break
        sleep(0.1)

with package_json_path.open('r') as f:
    version = load(f)['version']

_version_numbers, *_version_append = version.split("-")
__version__ = tuple(int(x) for x in _version_numbers.split(".")) + (*_version_append, )

SUPPORTED_FLAVORS: Set[str] = {'mastodon', 'misskey'}
registered_docs: Set[str] = set()
registered_flavors: Set[str] = set()


def bool_or_none(value: str) -> Optional[bool]:
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    return None


class FediverseCommentDirective(SphinxDirective):
    has_content = True
    option_spec = {
        'enable_post_creation': bool_or_none,
        'raise_error_if_no_post': bool_or_none,
        'replace_index_with_slash': bool_or_none,
        'token_names': str,
        'fedi_flavor': str,
        'fedi_username': str,
        'fedi_instance': str,
        'comments_mapping_file': str,
        'fetch_depth': int,
        'section_title': str,
        'section_level': int,
        'comment_id': str,
    }
    optional_arguments = len(option_spec)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.enable_post_creation: Optional[bool] = self.options.get(
            'enable_post_creation',
            self.env.config.enable_post_creation
        )
        self.raise_error_if_no_post: Optional[bool] = self.options.get(
            'raise_error_if_no_post',
            self.env.config.raise_error_if_no_post
        )
        self.replace_index_with_slash: Optional[bool] = self.options.get(
            'replace_index_with_slash',
            self.env.config.replace_index_with_slash
        )
        self.fedi_flavor: str = self.options.get(
            'fedi_flavor',
            self.env.config.fedi_flavor
        )
        self.fedi_username: str = self.options.get(
            'fedi_username',
            self.env.config.fedi_username
        )
        self.fedi_instance: str = self.options.get(
            'fedi_instance',
            self.env.config.fedi_instance
        )
        self.comments_mapping_file: str = self.options.get(
            'comments_mapping_file',
            self.env.config.comments_mapping_file
        )
        self.token_names: List[str] = self.options.get(
            'token_names',
            'MISSKEY_ACCESS_TOKEN'
            if self.fedi_flavor == 'misskey' else
            'MASTODON_CLIENT_ID,MASTODON_CLIENT_SECRET,MASTODON_ACCESS_TOKEN'
        ).split(',')
        self.fetch_depth: int = self.options.get(
            'fetch_depth',
            self.env.config.comment_fetch_depth
        )
        self.section_level: int = self.options.get(
            'section_level',
            self.env.config.comment_section_level
        )
        self.section_title: int = self.options.get(
            'section_title',
            self.env.config.comment_section_title
        )
        self.post_id: Optional[str] = self.options.get('post_id')
        if not (1 <= self.section_level <= 6):
            raise ValueError(f"Section level out of bounds: {self.section_level} not in range(1, 7)")

    def process_post(self, post_url: str, title: str) -> str:
        """Post a new comment on Mastodon and return the post ID."""
        if not self.enable_post_creation:
            if not self.raise_error_if_no_post:
                return ''
            elif input('Would you like to create the post yourself, and provide the ID? (y/N) ').lower()[0] == 'y':
                return input("Enter the ID and NOTHING ELSE: ")
            else:
                raise RuntimeError(f"Post creation is disabled. Cannot create a post for {post_url}")
        elif self.fedi_flavor == 'mastodon':
            return self.process_mastodon(post_url, title)
        elif self.fedi_flavor == 'misskey':
            return self.process_misskey(post_url, title)
        raise EnvironmentError(f"Unknown fediverse flavor selected. Supported: {SUPPORTED_FLAVORS}")

    def process_mastodon(self, post_url: str, title: str) -> str:
        from mastodon import Mastodon

        if not all(getenv(token) for token in self.token_names):
            raise EnvironmentError("Must provide all 3 mastodon access tokens")
        else:
            api = Mastodon(
                api_base_url=self.fedi_instance,
                client_id=getenv(self.token_names[0]),
                client_secret=getenv(self.token_names[1]),
                access_token=getenv(self.token_names[2]),
                user_agent=f'Sphinx-Fediverse v{".".join(str(x) for x in __version__)}',
            )
            message = f"Discussion post for {title}\n\n{self.env.config.html_baseurl}"
            message.rstrip('/')
            message += '/'
            message += post_url
            post = api.status_post(
                status=message, visibility='public', language='en',
            )
            return cast(str, post.id)

    def process_misskey(self, post_url: str, title: str) -> str:
        from misskey import Misskey

        if not getenv(*self.token_names):
            raise EnvironmentError("Must provide misskey access token")
        else:
            api = Misskey(
                self.fedi_instance,
                i=getenv(*self.token_names),
                # user_agent=f'Sphinx-Fediverse v{'.'.join(str(x) for x in __version__)}',
            )
            escaped_url = post_url.replace(')', r'\)')
            url = f"{self.env.config.html_baseurl.rstrip('/')}/{escaped_url}"
            message = f"Discussion post for [{title}]({url})"
            post = api.notes_create(
                text=message, visibility='public',
            )
            return cast(str, post['createdNote']['id'])

    def create_post_if_needed(self, post_url: str) -> str:
        """Check if a post exists for this URL. If not, create one."""
        if self.post_id is not None:
            return self.post_id

        # Read the mapping file
        mapping_file_path = Path(self.comments_mapping_file)
        if not mapping_file_path.exists():
            # File doesn't exist, create an empty mapping
            mapping: Dict[str, str] = {}
        else:
            with open(mapping_file_path, "r") as f:
                mapping = load(f)

        # Check if this URL already has a post ID
        if post_url in mapping:
            return mapping[post_url]

        # If not, create the post
        for node in self.state.document.traverse(nodes.title):
            title = node.astext()
            break  # accept the first title seen

        post_id = self.process_post(post_url, title)
        if post_id:
            mapping[post_url] = post_id
            # Save the updated mapping back to the file
            with open(mapping_file_path, "w") as f:
                dump(mapping, f, indent=2)

        return post_id

    def run(self) -> List[nodes.raw]:
        """Main method to execute the directive."""
        # Fetch base URL from conf.py (html_baseurl)
        if self.env.app.builder.name != 'html':
            raise EnvironmentError("Cannot function outside of html build")

        if not self.config.html_baseurl:
            raise ValueError("html_baseurl must be set in conf.py for Fediverse comments to work.")

        # Get the final output document URL using base_url + docname
        docname = self.env.docname
        if docname in registered_docs:
            raise RuntimeError("Cannot include two comments sections in one document")
        registered_docs.add(docname)

        # Handle special case for index.html and use configurable URL format
        if docname == "index":
            if self.replace_index_with_slash:
                post_url = "/"  # Replace index.html with just a slash
            else:
                post_url = "index.html"  # Keep the index.html
        else:
            post_url = docname + ".html"  # Always use .html extension

        # Create or retrieve the post ID
        post_id = self.create_post_if_needed(post_url)

        if post_id is None:
            return []

        # Add scripts
        self.state.document.settings.env.app.add_js_file(f'fedi_script_{self.fedi_flavor}.min.js')
        if self.fedi_flavor == 'misskey':
            self.state.document.settings.env.app.add_js_file('marked.min.js')

        # Create the DOM element to store the post ID
        post_id_node = nodes.raw('', f"""
            <div style="display:none;">
                <span id="fedi-post-id">{post_id}</span>
                <span id="fedi-instance">{self.fedi_instance}</span>
                <span id="fedi-flavor">{self.fedi_flavor}</span>
            </div>
            <h{self.section_level}>
                {self.section_title}
                <span class="comments-info">
                    <img class="fedi-icon" src="{self.env.config.html_baseurl}/_static/boost.svg" alt="Boosts">
                    <span id="global-reblogs"></span>,
                    <img class="fedi-icon" src="{self.env.config.html_baseurl}/_static/like.svg" alt="Likes">
                    <span id="global-likes"></span>
                </span>
            </h{self.section_level}>
            <div id="comments-section"></div>
            <script>
            document.addEventListener("DOMContentLoaded", function () {{
                const postIdElement = document.getElementById('fedi-post-id');
                const fediInstanceElement = document.getElementById('fedi-instance');
                if (postIdElement && fediInstanceElement) {{
                    const postId = postIdElement.textContent || postIdElement.innerText;
                    if (postId) {{
                        const fediInstance = fediInstanceElement.textContent || fediInstanceElement.innerText;
                        setImageLink("{self.env.config.html_baseurl}/_static/boost.svg")
                        fetchComments('{self.fedi_flavor}', fediInstance, postId, {self.fetch_depth});
                    }}
                }}
            }});
            </script>
        """, format='html')

        # Add the post ID element to the document
        self.add_name(post_id_node)
        return [post_id_node]


def on_builder_inited(app: Sphinx) -> None:
    if app.builder.name != 'html':
        return
    for file_path in Path(__file__).parent.joinpath('_static').iterdir():
        if file_path.is_file():
            out_path = Path(app.builder.outdir, f'_static/{file_path.name}')
            out_path.parent.mkdir(exist_ok=True, parents=True)
            copyfile(file_path, out_path)
    if Path(app.config.comments_mapping_file).exists():
        copyfile(
            app.config.comments_mapping_file,
            Path(app.builder.outdir, '_static', app.config.comments_mapping_file)
        )


def setup(app: Sphinx) -> Dict[str, Union[str, bool]]:
    # Register custom configuration options
    app.add_config_value('fedi_flavor', '', 'env')
    app.add_config_value('fedi_username', '', 'env')
    app.add_config_value('fedi_instance', '', 'env')
    app.add_config_value('enable_post_creation', True, 'env')
    app.add_config_value('comments_mapping_file', 'comments_mapping.json', 'env')
    app.add_config_value('replace_index_with_slash', True, 'env')
    app.add_config_value('raise_error_if_no_post', True, 'env')
    app.add_config_value('comment_fetch_depth', 5, 'env')
    app.add_config_value('comment_section_level', 2, 'env')
    app.add_config_value('comment_section_title', 'Comments', 'env')

    app.add_directive('fedi-comments', FediverseCommentDirective)
    app.connect('builder-inited', on_builder_inited)

    app.config.html_js_files.append('purify.min.js')
    app.config.html_js_files.append('fedi_script.min.js')
    app.config.html_css_files.append('fedi_layout.css')

    return {
        'version': '.'.join(str(x) for x in __version__),
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
