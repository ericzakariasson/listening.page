from nltk import tokenize

PUNCTUATION_MARKS = ('. ','? ','! ')


class TextChunker():
    """
    A class for chunking long text into smaller chunks.

    Parameters
    ----------
    maxlen : int
        The maximum length (in characters) of each chunk.

    Methods
    -------
    chunk(text)
        Divide the input text into smaller chunks no longer than `maxlen`. If a chunk is longer than `maxlen`, it is split into smaller chunks separated by a newline character or punctuation marks.

    Example
    -------
    >>> chunker = TextChunker(maxlen=1000)
    >>> for chunk in chunker.chunk(text):
    ...     print(chunk)
    """

    def __init__(self, maxlen):
        self.maxlen = maxlen

    def chunk(self, text):
        """
        Divide the input text into smaller chunks no longer than `maxlen`. If a chunk is longer than `maxlen`, it is split into smaller chunks separated by a newline character or punctuation marks.

        Parameters
        ----------
        text : str
            The text to be chunked.

        Yields
        ------
        str
            A smaller chunk of the input text, no longer than `maxlen`.

        Example
        -------
        >>> chunker = TextChunker(maxlen=1000)
        >>> for chunk in chunker.chunk(text):
        ...     print(chunk)
        """

        end=0
        while len(text) > self.maxlen and end != -1:
            # split paragraphs
            end = text[:self.maxlen].rfind('\n')
            # if a paragraph is longer than maxlen: split sentences
            if end == -1:
                end = max([text[:self.maxlen].rfind(m) for m in PUNCTUATION_MARKS])
                # if a sentence is longer than maxlen: split words
                if end == -1:
                    end = text[:self.maxlen].rfind(' ')
                    # if a word is longer than maxlen: force split
                    if end == -1:
                        end = self.maxlen-1

            yield text[:end+1]
            text = text[end+1:]
        yield text


def paragraphs(text):
    """
    Generator function that splits the given text into paragraphs.

    Parameters
    ----------
    text : str
        The input text to be divided into paragraphs.

    Yields
    ------
    str
        A paragraph from the input text.

    Example
    -------
    >>> text = "This is the first paragraph.\n\nThis is the second paragraph."
    >>> for paragraph in paragraphs(text):
    ...     print(paragraph)
    This is the first paragraph.
    This is the second paragraph.
    """
    for paragraph in text.splitlines():
        if paragraph:
            yield paragraph


def sentences(text):
    """
    Generator function that splits the given text into sentences.

    Parameters
    ----------
    text : str
        The input text to be divided into sentences.

    Yields
    ------
    str
        A sentence from the input text.

    Example
    -------
    >>> text = "This is the first sentence. This is the second sentence."
    >>> for sentence in sentences(text):
    ...     print(sentence)
    This is the first sentence.
    This is the second sentence.
    """
    for s in tokenize.sent_tokenize(text):
        if s:
            yield s


if __name__ == '__main__':
    with open('test_text.txt','r') as ft:
        text = ft.read()

    chunk = TextChunker(1500)
    cum=0
    for i, line in enumerate(chunk.chunk(text)):
        print(line)
        cum += len(line)
        print(i,len(line),cum)
        print("==========")

    print(len(text))
