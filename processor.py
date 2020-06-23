import copy


class MyMatrix:

    def __init__(self, matrix=[]):
        self.dim = None
        self.rows = None
        self.cols = None
        self.matrix = matrix

    def __del__(self):
        self.matrix.clear()
        del self

    def input_matrix(self, word=''):
        dim = [int(i) for i in input(f'Enter size of {word}matrix: ').split()]
        self.dim = dim
        self.rows = dim[0]
        self.cols = dim[1]
        print(f'Enter {word}matrix: ')
        temp = [[col for col in input().split()] for raw in range(self.rows)]
        try:
            self.matrix = [[int(col) for col in raw] for raw in temp]
        except ValueError:
            self.matrix = [[float(col) for col in raw] for raw in temp]

    def add(self, matrix2):
        if self.dim != matrix2.dim:
            return 'ERROR'

        return [[self.matrix[r][c] + matrix2.matrix[r][c] for c in range(self.cols)] for r in range(self.rows)]

    def display_matrix(self, res=False):
        if res:
            print('The result is:')
        print(*[" ".join([str(n) for n in row]) for row in self.matrix], sep="\n")  # round(n, 2) if n % 1 != 0 else round(n)
    def mult(self, c):
        if type(c) != MyMatrix:
            return [[self.matrix[n][m] * c for m in range(self.cols)] for n in range(self.rows)]
        else:
            if self.cols == c.rows:
                s = 0
                t = []
                res = MyMatrix()
                for z in range(self.rows):
                    for j in range(c.cols):
                        for i in range(self.cols):
                            s += self.matrix[z][i] * c.matrix[i][j]
                        t.append(s)
                        s = 0
                    res.matrix.append(t)
                    t = []
                return res.matrix[:]

            else:
                return 'ERROR'

    def transp(self, transp_type):
        temp = MyMatrix(self.matrix)
        if transp_type == 'main':
            self.matrix = [[temp.matrix[m][n] for m in range(self.cols)] for n in range(self.rows)]
        elif transp_type == 'side':
            self.matrix = [[temp.matrix[self.cols - 1 - m][self.rows - 1 - n] for m in range(self.cols)] for n in
                           range(self.rows)]
        elif transp_type == 'vert':
            self.matrix = [[temp.matrix[n][self.cols - 1 - m] for m in range(self.cols)] for n in range(self.rows)]
        elif transp_type == 'horiz':
            self.matrix = [[temp.matrix[self.rows - 1 - n][m] for m in range(self.cols)] for n in range(self.rows)]

    def minor(self, j, i=0):
        m1 = MyMatrix(copy.deepcopy(self.matrix))

        current_row = m1.matrix.pop(i)
        m1.rows = self.rows - 1

        for n in range(m1.rows):
            m1.matrix[n].pop(j)
        m1.cols = self.cols - 1

        return (-1)**(i+j) * current_row[j] * m1.det()

    def minor_ad(self, j, i=0):
        m = MyMatrix(copy.deepcopy(self.matrix))

        m.matrix.pop(i)
        m.rows = self.rows - 1

        for n in range(m.rows):
            m.matrix[n].pop(j)
        m.cols = self.cols - 1

        return (-1)**(i+j) * m.det()

    def det(self):
        if self.rows == 1:
            return self.matrix[0][0]
        if self.rows == 2:
            return self.matrix[0][0]*self.matrix[1][1] - self.matrix[0][1]*self.matrix[1][0]

        res = 0
        for j in range(self.cols):
            res += self.minor(j=j)
        return res


# End of class MyMatrix


def menu(div):
    menu_divs = {
        "main_menu": """
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit""",
        "transp_menu": """
1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line"""
    }

    print(menu_divs[div])


# Menu functions
def addition():
    m1 = MyMatrix()
    m1.input_matrix('first ')

    m2 = MyMatrix()
    m2.input_matrix('second ')

    res = m1.add(m2)
    if res != 'ERROR':
        m3 = MyMatrix(res)
        m3.display_matrix(True)
    else:
        print('The operation cannot be performed.')


def multipl_const():
    m = MyMatrix()
    m.input_matrix()

    c = input('Enter constant: ')
    try:
        c = int(c)
    except ValueError:
        c = float(c)
    m.matrix = m.mult(c)
    m.display_matrix(True)


def multipl_matr():
    m1 = MyMatrix()
    m1.input_matrix('first ')

    m2 = MyMatrix()
    m2.input_matrix('second ')

    res = m1.mult(m2)
    if res != 'ERROR':
        m3 = MyMatrix(m1.mult(m2))
        m3.display_matrix(True)
    else:
        print('The operation cannot be performed.')


def transposition_():
    def transposition_case(arg):
        switcher = {
            1: 'main',
            2: 'side',
            3: 'vert',
            4: 'horiz'
        }
        return switcher.get(arg)

    menu('transp_menu')
    transp_type = transposition_case(int(input('Your choice: ')))

    m = MyMatrix()
    m.input_matrix()

    m.transp(transp_type)
    m.display_matrix(True)


def determinant():
    m = MyMatrix()
    m.input_matrix()

    print('The result is:')
    print(round(m.det(), 2))


def inverse():
    m = MyMatrix()
    m.input_matrix()

    det = m.det()
    if det == 0:
        print("This matrix doesn't have an inverse.")
        return

    m_inv = MyMatrix()
    m_inv.rows = m.rows
    m_inv.cols = m.cols
    m_inv.matrix = [[m.minor_ad(i=i, j=j) for j in range (m_inv.cols)]for i in range(m_inv.rows)]

    m_inv.transp('main')
    m_inv.matrix = m_inv.mult(1/det)

    m_inv.display_matrix(True)

# ***
def main():
    menu('main_menu')

    def main_case(arg):
        switcher = {
            1: addition,
            2: multipl_const,
            3: multipl_matr,
            4: transposition_,
            5: determinant,
            6: inverse
        }
        if arg == 0:
            return 0
        func = switcher.get(arg)
        func()
        return True

    return main_case(int(input('Your choice: ')))


# ***
if __name__ == '__main__':
    while main():
        pass
