from typing import List
from haystack import component, Document

@component
class NullCharacterReplacer:
  """
  A component for replacing null characters by the � character
  """
  @component.output_types(documents=List[Document])
  def run(self, documents:List[Document]):
      ret_docs = []
      for d in documents:
          d.content = d.content.replace("\x00", " ")
          ret_docs.append(d)
      return {"documents": ret_docs}