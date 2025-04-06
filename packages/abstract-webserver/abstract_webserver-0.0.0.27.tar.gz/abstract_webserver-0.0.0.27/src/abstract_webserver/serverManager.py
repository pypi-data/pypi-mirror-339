from .abstract_types import *
from typing import *
from abstract_utilities import *
import json
from pathlib import Path
def dirname_to_it(string,directory):
    if string in directory:
        while True:
            basename = os.path.basename(directory)
            if string in basename:
                return directory
            prior_dir = directory
            directory = os.path.dirname(directory)
            if directory == prior_dir:
                return
            print(directory)
def is_valid_path(path: Path):
    # Exclude paths that start with the GVFS mount point
    if str(path).startswith("/run/user/1000/gvfs/"):
        return False
    try:
        return path.is_dir()
    except OSError:
        return False
def find_src_dir(substr='src', directory=None):
    """
    Searches for a directory whose name contains `substr` by first checking
    the given directory and its ancestors. If not found, recursively searches
    within the directory tree.
    """
    base_dir = Path(directory) if directory else Path.cwd()
    
    # Check the base directory and its parents
    for parent in [base_dir] + list(base_dir.parents):
        if substr in parent.name:
            return parent
    
    # If not found, search recursively in the directory tree
    for path in base_dir.rglob('*'):
        if is_valid_path(path) and substr in path.name:
            return path
    return None
def get_domain_from_src(directory=None):
    src_dir = find_src_dir(directory=directory)
    directory = os.path.dirname(src_dir)
    domain  = os.path.basename(directory)
    domain,ext = os.path.splitext(domain)
    if not domain.startswith('http'):
        domain = f'https://{domain}'
    domain = f'{domain}{ext or ".com"}'
    return domain
class serverManager(metaclass=SingletonMeta):
    def __init__(self, src_dir=None,domain=None,imgs_dir=None,fb_id=None,directory=None):
        """Initialize the file directory manager with base paths."""
        self.src_dir = src_dir or find_src_dir(directory=directory)
        self.domain = domain or get_domain_from_src(directory=self.src_dir or directory)
        self.pages_dir = os.path.join(self.src_dir, "pages")
        self.json_dir = os.path.join(self.src_dir, "json_pages")
        self.contents_dir = os.path.join(self.src_dir, "contents")
        self.public_dir = os.path.join(self.src_dir, "../public")
        self.imgs_dir = imgs_dir or os.path.join(self.public_dir,'imgs')
        self.fb_id = fb_id
        self.ensure_directories()

    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        for directory in [self.pages_dir, self.json_dir, self.contents_dir, self.public_dir]:
            os.makedirs(directory, exist_ok=True)

    def join_path(self, *paths: str) -> str:
        """Join multiple path segments into a single path."""
        return os.path.join(*paths)

    def get_file_paths(self, directory: str, filename: str, is_index: bool = False) -> Tuple[str, str, str]:
        """Generate paths for JSON, page, and content files based on directory and filename."""
        json_path = self.join_path(self.json_dir, directory, f"{filename}.json") if directory else self.join_path(self.json_dir, f"{filename}.json")
        pages_path = self.join_path(self.pages_dir, "home", f"{filename}.tsx") if is_index else self.join_path(self.pages_dir, directory, f"{filename}.tsx")
        contents_path = self.join_path(self.contents_dir, directory, f"{filename}.md") if directory else self.join_path(self.contents_dir, f"{filename}.md")
        return json_path, pages_path, contents_path

    def read_json(self, json_path: str) -> dict:
        """Read and parse a JSON file."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading {json_path}: {e}")
            return {}

    def write_to_file(self, contents: str, file_path: str) -> None:
        """Write contents to a file, creating directories if needed."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(contents)

    def extract_content_to_md(self, json_data: dict, contents_path: str) -> Optional[str]:
        """Extract content from JSON and save it as a Markdown file."""
        content = json_data.get("content")
        if not content:
            print(f"No content found in JSON for {contents_path}")
            return None
        self.write_to_file(content.strip(), contents_path)
        return contents_path

    def update_json(self, json_path: str, content_file: str) -> None:
        """Update JSON to reference the content file instead of embedding content."""
        json_data = self.read_json(json_path)
        if "content" in json_data:
            del json_data["content"]
            relative_content_path = os.path.relpath(content_file, self.src_dir).replace("\\", "/")
            json_data["content_file"] = relative_content_path
            self.write_to_file(json.dumps(json_data, indent=4), json_path)

    def generate_tsx_template(self, filename: str, directory: str, meta: dict, is_index: bool = False) -> str:
        """Generate TSX template for a page."""
        add_imports = ""
        json_path, pages_path, contents_path = self.get_file_paths(directory, filename, is_index=True)
        pdfViewer = meta.get('pdfViewer') or 'false'
        dirname = os.path.basename(directory) if directory else "home"  # Use 'home' for index
        base_name = filename.replace('-', '_')
        page_name = f"Page_{base_name}" if base_name[0].isdigit() else f"{base_name.capitalize()}Page"
        sources_name = f"{page_name}Sources"
        return f"""import {{ GetStaticProps, NextPage }} from 'next';
import Head from 'next/head';
import path from 'path';
import fs from 'fs';
import {{ generateFullPageMetadata }} from '@MetaHead';
import {{ build_content }} from '@functions';
import {{ ImageData, PageData, SourceProps }} from '@interfaces';
import PageHeader from '@PageHeader';
import Body from '@Body';

const {sources_name}: NextPage<SourceProps> = ({{ metadataHTML, pageData, imageData }}) => {{
  return (
    <>
      <Head>
        <meta charSet="UTF-8" />
        <link rel="icon" href="/imgs/favicon.ico" type="image/x-icon"/>
        <meta property="og:image" content={{imageData['social_meta']['og:image']}}/>
        <meta property="og:url" content={{pageData.share_url}}/>
        <meta property="og:type" content="article"/>
        <meta property="og:title" content={{pageData.title}}/>
        <meta property="og:description" content={{pageData.description}}/>
        <meta property="fb:app_id" content="{self.fb_id}"/>
        <title>{{pageData.title}}</title>
        <div dangerouslySetInnerHTML={{{{ __html: metadataHTML }}}} />
      </Head>
      <PageHeader meta={{pageData}} baseUrl={{pageData.BASE_URL}} />
      <Body meta={{pageData}} pdfViewer={{pageData?.pdfViewer}} />
    </>
  );
}};

export const getStaticProps: GetStaticProps<SourceProps> = async () => {{
  try {{
    const filename = '{filename}';
    const jsonPath = '{json_path}'
    const contentsPath = '{contents_path}'
    const pagesPath ='{pages_path}'

    const jsonContents = fs.readFileSync(jsonPath, 'utf8');
    const pageData: PageData = JSON.parse(jsonContents);
    const thumbnailPath = path.join(pageData.thumbnail, 'info.json');
    
    const imageContents = fs.readFileSync(thumbnailPath, 'utf8');
    const imageData = JSON.parse(imageContents);
    pageData.imageData = imageData;

    const pageContents = fs.readFileSync(contentsPath, 'utf8');
    const pageContent = await build_content(pageContents, pageData, '{dirname if directory else ""}');
    pageData.content = pageContent;

    const {{ toHTML }} = generateFullPageMetadata(pageData, imageData);
    const metadataHTML = toHTML();

    return {{
      props: {{
        metadataHTML,
        pageData,
        imageData
      }},
    }};
  }} catch (error) {{
    console.error('Error in getStaticProps:', error);
    return {{
      notFound: true,
    }};
  }}
}};

export default {sources_name};
        """

    def process_directory(self, directory: str) -> None:
        """Process all JSON files in a directory."""
        json_directory = self.join_path(self.json_dir, directory)
        if not os.path.isdir(json_directory):
            print(f"Directory not found: {json_directory}")
            return

        for item in os.listdir(json_directory):
            filename, ext = os.path.splitext(item)
            if ext.lower() != ".json":
                continue

            is_index = (directory == "" and filename == "index")  # Check if it's the root index
            json_path, pages_path, contents_path = self.get_file_paths(directory, filename, is_index)
            json_data = self.read_json(json_path)

            # Extract content to Markdown
            content_file = self.extract_content_to_md(json_data, contents_path)
            if content_file:
                self.update_json(json_path, content_file)
    
            # Generate or update TSX page
            tsx_content = self.generate_tsx_template(filename, directory, json_data, is_index)
            self.write_to_file(tsx_content, pages_path)
            print(f"Processed: {json_path} -> {contents_path}, {pages_path}")

    def process_root_index(self) -> None:
        """Process the root index.json file separately."""
        json_path = self.join_path(self.json_dir, "index.json")
        if not os.path.exists(json_path):
            print(f"Root index.json not found: {json_path}")
            return

        filename = "index"
        directory = ""  # Empty directory for root-level index
        json_data = self.read_json(json_path)
        json_path, pages_path, contents_path = self.get_file_paths(directory, filename, is_index=True)

        # Extract content to Markdown
        content_file = self.extract_content_to_md(json_data, contents_path)
        if content_file:
            self.update_json(json_path, content_file)

        # Generate TSX page at /home/index.tsx
        tsx_content = self.generate_tsx_template(filename, directory, json_data, is_index=True)
        self.write_to_file(tsx_content, pages_path)
        print(f"Processed root index: {json_path} -> {contents_path}, {pages_path}")

    def process_all(self) -> None:
        """Process all directories in json_pages and the root index.json."""
        # Process root index.json first
        self.process_root_index()

        # Process all directories
        for directory in os.listdir(self.json_dir):
            if os.path.isdir(self.join_path(self.json_dir, directory)):
                self.process_directory(directory)
