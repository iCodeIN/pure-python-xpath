import re

class XPATHTokenizer:

    def __init__(self):
        self.left_brackets = ['(','{','[']
        self.right_brackets = [')','}',']']
        self.operators = ['contains', 'ends-with', 'length', 'not', 'starts-with', 'text', '=', '!=', '<=', '<', '>=', '>', 'or', 'and', '//', '/', '*']
        self.html_tags = ['a', 'abbr', 'acronym', 'address', 'applet', 'area', 'article', 'aside', 'audio',
                 'b', 'base', 'basefont', 'bb', 'bdo', 'big', 'blockquote', 'body', 'br', 'button',
                 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'command',
                 'datagrid', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl', 'dt',
                 'em', 'embed', 'eventsource',
                 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'form', 'frame', 'frameset',
                 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hroup', 'hr', 'html',
                 'i', 'iframe', 'img', 'input', 'ins', 'isindex',
                 'kbd', 'keygen',
                 'label', 'legend', 'li', 'link',
                 'map', 'mark', 'menu', 'meta', 'meter',
                 'nav', 'noframes', 'noscript',
                 'object', 'ol', 'optgroup', 'option', 'output',
                 'p', 'param', 'pre', 'progress',
                 'q',
                 'rp', 'rt', 'ruby',
                 's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strike', 'strong',
                 'style', 'sub', 'sup',
                 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'tt',
                 'u', 'ul',
                 'var', 'video',
                 'wbr']

    def _check_brackets(self, xpath_expression):

        # check bracket nesting
        stk = []
        for i in range(0, len(xpath_expression)):
            t = xpath_expression[i]
            if t in self.left_brackets:
                stk.append(t)
                continue

            if t in self.right_brackets:

                # check if there is left bracket
                if len(stk) == 0:
                    raise SyntaxError('Invalid XPATH')

                # check whether the left bracket matches
                left_bracket_index = self.left_brackets.index(stk[-1])
                right_bracket_index = self.right_brackets.index(t)
                if left_bracket_index != right_bracket_index:
                    raise SyntaxError('Mismatched brackets in XPATH')

                # pop bracket
                stk.pop(-1)


    def tokenize_expression(self, xpath_expression):

        # check brackets
        self._check_brackets(xpath_expression)

        # greedy tokenization strategy
        tokens = []

        while xpath_expression != '':
            token_candidates = [
                ',' if xpath_expression.startswith(',') else '',
                max([x for x in (self.right_brackets + self.left_brackets) if xpath_expression.startswith(x)] + [''], key=len),
                max([x for x in self.operators if xpath_expression.startswith(x)] + [''], key=len),
                max([x for x in self.html_tags if xpath_expression.startswith(x)] + [''], key=len),
                re.compile('^@[a-zA-Z0-9-]+').match(xpath_expression).group(0) if re.compile('^@[a-zA-Z0-9-]+').match(xpath_expression) else '',
                re.compile('^\'[^\']+\'').match(xpath_expression).group(0) if re.compile('^\'[^\']+\'').match(xpath_expression) else '',
                re.compile('^[0-9]+').match(xpath_expression).group(0) if re.compile('^[0-9]+').match(xpath_expression) else '',
                ' ' if re.compile('^ +').match(xpath_expression) else '',
            ]
            token = max(token_candidates, key=len)
            if token == '':
                raise SyntaxError('Unable to process XPATH expression. Invalid/unknown token for sub-string {}'.format(xpath_expression))
            tokens.append(token)
            xpath_expression = xpath_expression[len(token):]

        # output
        return tokens