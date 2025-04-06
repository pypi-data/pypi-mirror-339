.. GraphRAG Documentation
   Created for GraphRAG document indexing and processing toolkit.

Welcome to GraphRAG Documentation!
=================================

GraphRAG is a document analysis and retrieval system that enhances traditional Retrieval-Augmented Generation (RAG) with knowledge graph capabilities. It's designed to process, index, and query complex document collections by combining vector-based retrieval with graph relationship context.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   modules
   api

Features
========

- **Document Processing**: Extract structured text from PDFs, text files, and other document formats
- **Knowledge Graph Construction**: Automatically extract entities and relationships
- **Timeline Analysis**: Create chronological sequences of events from documents
- **Graph-based Retrieval**: Enhance document retrieval with graph relationships
- **Batch Processing**: Process large document collections efficiently

Installation
===========

.. code-block:: bash

   pip install -e .

For development:

.. code-block:: bash

   pip install -e ".[test]"

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
