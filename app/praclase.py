import subprocess

import click
from lsprotocol.types import (TEXT_DOCUMENT_COMPLETION, CompletionItem,
                              CompletionList, CompletionOptions,
                              CompletionParams)
from pygls.server import LanguageServer

@click.command()
@click.option('-d', '--dictionary', type=click.Path(), required=True, help='Path to the dictionary file')
@click.option('-c', '--dictionary_executable', type=click.Path(), required=True, help='Path to the dictionary executable')
@click.option('-l', '--lexicon', type=click.Path(), required=True, help='Path to the lexicon file')
@click.option('-x', '--lexicon_executable', type=click.Path(), required=True, help='Path to the lexicon executable')
def cli(dictionary, dictionary_executable, lexicon, lexicon_executable):
    def suggestions(line):
        p = subprocess.run(
            [dictionary_executable, dictionary],
            input=line,
            capture_output=True,
            text=True,
        )

        response = list(
            map(
                lambda suggestion: CompletionItem(label=suggestion),
                p.stdout.splitlines(),
            )
        )

        return response


    def lookup(query):
        p = subprocess.run(
            [lexicon_executable, lexicon],
            input=query,
            capture_output=True,
            text=True,
        )
        if query[0].isupper():
            response = list(
                map(
                    lambda suggestion: CompletionItem(label=suggestion.capitalize()),
                    p.stdout.splitlines(),
                )
            )
        else:
            response = list(
                map(
                    lambda suggestion: CompletionItem(label=suggestion),
                    p.stdout.splitlines(),
                )
            )

        return response


    def get_last_word(input_string):
        words = input_string.split()
        if words:
            return words[-1]
        else:
            return None

    server = LanguageServer("praclase", "v0.1.0")

    @server.feature(TEXT_DOCUMENT_COMPLETION, CompletionOptions(trigger_characters=[" "]))
    def completions(params: CompletionParams):
        items = []
        document = server.workspace.get_document(params.text_document.uri)
        current_line = document.lines[params.position.line]
        last_word = get_last_word(current_line)

        if params.context != None and params.context.trigger_character == " ":
            items = suggestions(current_line)
        elif last_word != None and len(last_word) > 3:
            items = suggestions(current_line) + lookup(last_word)
        else:
            items = suggestions(current_line)

        return CompletionList(is_incomplete=False, items=items)


    server.start_io()

if __name__ == "__main__":
    cli()
