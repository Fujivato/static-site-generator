# How we will process Markdown Documents

Since decomposition is an integral part of building software solutions, this markdown document provides some insight into my general strategy for processing markdown blocks into HTML nodes.

## What's the aim?

We want out static site generator to be able to take a markdown text string and produce a list of HTMLNodes that can be composed in an HTML DOM.

## How will we achieve this?

***First***, we will start by looking at what functions we have written so far.

***Next***, we will look at what functions we may need to process certain markdown block types that we have not yet written.

***Finally*** we will describe the order in which we will process blocks and what actions we will take per block type.

## What functions have we got?

- Convert text nodes to HTML (leaf) nodes
- Split text nodes to specific "text type" nodes
- Identify markdown images
- Extract markdown image nodes from text string
- Identify markdown links
- Extract markdown link nodes from text string
- Convert plain text strings to TextNodes
- Extract markdown blocks
- Identify markdown blocks

## What functions do we need?

- [x] Extract markdown quote blocks
- [x] Extract markdown UL blocks
- [x] Extract markdown OL blocks
- [x] Extract markdown code blocks
- [x] Extract markdown Headings

## Processing block types

### How will we process?
We will process all block types in order and add to a dynamic list of HTMLNodes that should result in an HTML document tree in the same structure as the original markdown document.

### Heading Blocks
Convert the markdown block into a leaf node with tag of h# based on md heading type and add to node list.

### Code Blocks
Convert the markdown block into a leaf node with tag of "code". Remove surrouding backticks and add to the node list.

### Quote Blocks
Convert the markdown block into a leaf node with tag of "blockquote". Remove starting > characters from each line of the quote and process each line of the quote to create *TextNodes*. 

### Unordered Lists
Convert the mardown block into leaf nodes with tags of "li". Process each list item to create *TextNodes*. Add to *ParentNode* with tag "ul".

### Ordered Lists
Convert the markdown block into leaf nodes with tags of "li". Process each 
list item to create *TextNodes*. Add to *ParentNode* with tag "ol".

### Paragraphs
Process the text to create bold, italic, bold italic, code, image and links. Add to *ParentNode* with tag "p".