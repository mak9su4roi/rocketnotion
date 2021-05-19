from notion.client import NotionClient
from notion.block import EmbedBlock


# "6140f87cf33ffbeee6ebeff24772ec4391fbdff8b87f96ee5ac876843c101c2be73d5c12c0f19a341d87929e52c6c7666afbec1603af3543350471afe02436230d4751f5cba0cec4bac37b554482"
# "https://www.notion.so/nerro-e3c8874ec4f74a11b78314a6ff1e67a0"
# "https://drive.google.com/uc?export=view&id=1vVBdVsxu0U_vXh7r-Rb05bWd0-2fi1Pi"
def embed(token, notebook, link):
    client = NotionClient(token_v2=token)
    page = client.get_block(notebook)
    newchild = page.children.add_new(EmbedBlock, title="notes", width=1000, height=1400)
    newchild.set_source_url(link)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    embed("6140f87cf33ffbeee6ebeff24772ec4391fbdff8b87f96ee5ac876843c101c2be73d5c12c0f19a341d87929e52c6c7666afbec1603af3543350471afe02436230d4751f5cba0cec4bac37b554482",
          "https://www.notion.so/nerro-e3c8874ec4f74a11b78314a6ff1e67a0",
          "https://drive.google.com/uc?export=view&id=1vVBdVsxu0U_vXh7r-Rb05bWd0-2fi1Pi")