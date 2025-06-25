import os
import argparse
import yaml

VAULT_PATH = "vault/lookup/rules/"

def parse_frontmatter(text):
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            front = text[3:end].strip()
            body = text[end + 3:].strip()
            try:
                data = yaml.safe_load(front)
                return data, body
            except yaml.YAMLError:
                return {}, text
    return {}, text

def search_rules(query=None, system=None, tag=None):
    results = []

    for dirpath, _, filenames in os.walk(VAULT_PATH):
        for fname in filenames:
            if fname.endswith(".md"):
                path = os.path.join(dirpath, fname)
                with open(path, 'r') as f:
                    content = f.read()
                    meta, body = parse_frontmatter(content)

                    if query and query.lower() not in body.lower():
                        continue
                    if system and not any(system.lower() in str(t).lower() for t in meta.get("tags", [])):
                        continue
                    if tag and not any(tag.lower() == str(t).lower() for t in meta.get("tags", [])):
                        continue

                    results.append({
                        "filename": fname,
                        "tags": meta.get("tags", []),
                        "content": body.strip()
                    })
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Markdown rules with optional system/tag filters.")
    parser.add_argument("query", type=str, nargs="?", help="Search term (optional)")
    parser.add_argument("--system", type=str, help="Filter by system in frontmatter tags")
    parser.add_argument("--tag", type=str, help="Filter by exact tag in frontmatter")
    parser.add_argument("--json", action="store_true", help="Return results as JSON")

    args = parser.parse_args()
    matches = search_rules(args.query, args.system, args.tag)

    if not matches:
        print("No match found.")
    else:
        if args.json:
            import json
            print(json.dumps(matches, indent=2))
        else:
            for match in matches:
                print(f"\n=== {match['filename']} ===")
                if match['tags']:
                    print(f"Tags: {', '.join(match['tags'])}")
                print(match['content'])

