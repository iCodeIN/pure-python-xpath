from xpath_syntax_tree import XPATHSyntaxTree


class XPATH:

    @staticmethod
    def xpath(xpath_expression, bs_doc):

        # convert to nodes
        nodes = XPATHSyntaxTree().xpath_to_syntax_tree(xpath_expression)

        # iteratively go through each node in the XPATH chain
        inp = ([bs_doc], [])
        for n in nodes:
            inp = n.evaluate(inp[0], inp[1])

        # empty list
        if len(inp) == 0:
            return []

        # if the first element is a list, we terminated at a non-leaf node
        # throw away the negative nodes and return only the first part of the
        # tuple
        if inp[0].__class__.__name__ == 'list':
            return inp[0]

        # else return the entire list
        else:
            return inp