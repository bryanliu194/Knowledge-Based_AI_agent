# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import numpy as np
import cv2


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.question_set2 = {}
        self.answer_set2 = {}
        self.question_set3 = {}
        self.answer_set3 = {}
        self.methods2x2 = [self.method2x2_compare_same, self.method2x2_mirror, self.method2x2_compare_diff, self.method2x2_ratio]
        self.methods3x3 = [self.method3x3_compare_same, self.method3x3_sum, self.method3x3_add, self.method3x3_add2, self.method3x3_sub, self.method3x3_common_area, self.method3x3_diff_ver, self.method3x3_diff_hor, self.method3x3_enlarge]
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.g = None
        self.h = None
        self.score = 0
        self.answer = 1

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.

    def Solve(self, problem):

        if problem.problemType == '2x2':
            # self.read_img(problem)
            self.read_img2(problem)
            for method in self.methods2x2:
                method()
                print(method)
                if self.score == 10:
                    break
        elif problem.problemType == '3x3':
            self.read_img3(problem)
            for method in self.methods3x3:
                method()
                if self.score == 10:
                    print(method)
                    break

        answer = self.answer
        print(f'answer {self.answer}')
        print(f'score {self.score}')
        self.__init__()
        return int(answer)

    def method3x3_compare_same(self):
        a, b, c, d, e, f, g, h = self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h
        if a == b and b == c:
            for key in self.answer_set3:
                ans = np.count_nonzero(self.answer_set3[key] < 255)
                if ans == g:
                    self.answer = key
                    self.score = 10

    def method3x3_sum(self):
        a, b, c, d, e, f, g, h = self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h
        best = 10000
        if (d + e + f)*0.95 < a + b + c < (d + e + f)*1.05:
            for key in self.answer_set3:
                ans = np.count_nonzero(self.answer_set3[key] < 255)
                if (g + h + ans) * 0.95 < a + b + c < (g + h + ans) * 1.05 and abs(a + b + c - (g + h + ans)) < best:
                    best = abs(a + b + c - (g + h + ans))
                    self.answer = key
                    self.score = 8
                if (g + h + ans) * 0.99 < a + b + c < (g + h + ans) * 1.01 and abs(a + b + c - (g + h + ans)) < best:
                    best = abs(a + b + c - (g + h + ans))
                    self.answer = key
                    self.score = 10

    def method3x3_add(self):
        A, B, C, G, H = self.question_set3['A'], self.question_set3['B'], self.question_set3['C'], self.question_set3['G'], self.question_set3['H']
        a, b, c, g, h = A - 255, B - 255, C - 255, G - 255, H - 255
        best = 10000
        c0 = a + b
        c0 = np.clip(c0, 0, 1)
        if np.count_nonzero(c - c0) < 400:
            for key in self.answer_set3:
                ans = self.answer_set3[key] - 255
                i = g + h
                i = np.clip(i, 0, 1)
                nonzero = np.count_nonzero(ans - i)
                if nonzero < 400 and nonzero < best:
                    best = nonzero
                    self.answer = key
                    self.score = 10

    def method3x3_add2(self):
        A, B, C, G, H = self.question_set3['A'], self.question_set3['B'], self.question_set3['C'], self.question_set3['G'], self.question_set3['H']
        a, b, c, g, h = A - 255, B - 255, C - 255, G - 255, H - 255
        best = 10000
        if np.count_nonzero(a - b - c) < 400:
            for key in self.answer_set3:
                ans = self.answer_set3[key] - 255
                nonzero = np.count_nonzero(g - h - ans)
                if nonzero < 400 and nonzero < best:
                    best = nonzero
                    self.answer = key
                    self.score = 10

    def method3x3_sub(self):
        A, B, C, G, H = self.question_set3['A'], self.question_set3['B'], self.question_set3['C'], self.question_set3['G'], self.question_set3['H']
        a, b, c, g, h = A - 255, B - 255, C - 255, G - 255, H - 255
        best = 10000
        sub = a - b
        if np.count_nonzero(sub - c) < 2500:
            for key in self.answer_set3:
                ans = self.answer_set3[key] - 255
                sub2 = g - h
                sub2[sub2 < 0] = 1
                nonzero = np.count_nonzero(sub2 - ans)
                if nonzero < 2500 and nonzero < best:
                    best = nonzero
                    self.answer = key
                    self.score = 10

    def method3x3_common_area(self):
        A, B, C, G, H = self.question_set3['A'], self.question_set3['B'], self.question_set3['C'], self.question_set3[
            'G'], self.question_set3['H']
        a, b, c, g, h = A - 255, B - 255, C - 255, G - 255, H - 255
        best = 100000
        a = a * 5
        g = g * 5
        c0 = a - b
        c0[c0 != 4] = 0
        c0[c0 == 4] = 1
        if np.count_nonzero(c0 - c) < 300:
            for key in self.answer_set3:
                ans = self.answer_set3[key] - 255
                c1 = g - h
                c1[c1 != 4] = 0
                c1[c1 == 4] = 1
                nonzero = np.count_nonzero(c1 - ans)
                if nonzero < 300 and nonzero < best:
                    best = nonzero
                    self.answer = key
                    self.score = 10

    def method3x3_diff_hor(self):
        a, b, c, d, e, f, g, h = self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h
        row1 = abs(a - b) + abs(b - c) + abs(a - c)
        best = 10000
        for key in self.answer_set3:
            ans = np.count_nonzero(self.answer_set3[key] < 255)
            row2 = abs(g-h) + abs(h-ans) + abs(g-ans)
            if abs(row1-row2) < 100 and abs(row1-row2) < best:
                best = abs(row1-row2)
                self.answer = key
                self.score = 10

    def method3x3_diff_ver(self):
        a, c, d, f, g = self.a, self.c, self.d, self.f, self.g

        for key in self.answer_set3:
            ans = np.count_nonzero(self.answer_set3[key] < 255)
            if (c-f)*0.95 < a-d < (c-f)*1.05 or abs(a-d - c+f) < 500:
                if (f-ans)*0.95 < d-g < (f-ans)*1.05 or abs(d-g - f+ans) < 500:
                    self.answer = key
                    self.score = 8
            if (c-f)*0.99 < a-d < (c-f)*1.01 or abs(a-d - c+f) < 200:
                if (f-ans)*0.99 < d-g < (f-ans)*1.01 or abs(d-g - f+ans) < 200:
                    self.answer = key
                    self.score = 10

    def method3x3_enlarge(self):
        a, b, c, d, e, f, g, h = self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h

        for key in self.answer_set3:
            ans = np.count_nonzero(self.answer_set3[key] < 255)
            if a == b or h == g:
                break

            if (ans - h)/(h - g)*0.5 < (c - b)/(b - a) < (ans - h)/(h - g)*1.5 and self.score < 2:
                self.score = 2
                self.answer = key

            if (ans - h)/(h - g)*0.8 < (c - b)/(b - a) < (ans - h)/(h - g)*1.2 and self.score < 4:
                self.score = 4
                self.answer = key

            if (ans - h)/(h - g)*0.9 < (c - b)/(b - a) < (ans - h)/(h - g)*1.1 and self.score < 6:
                self.score = 6
                self.answer = key

            if (ans - h)/(h - g)*0.95 < (c - b)/(b - a) < (ans - h)/(h - g)*1.05 and self.score < 8:
                self.score = 8
                self.answer = key

    def read_img3(self, problem):
        for key in problem.figures:
            img = cv2.imread(problem.figures[key].visualFilename)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            _, threshold = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

            if ord(key) >= ord("A"):
                self.question_set3[key] = threshold
            else:
                self.answer_set3[key] = threshold

        self.a = np.count_nonzero(self.question_set3['A'] < 255)
        self.b = np.count_nonzero(self.question_set3['B'] < 255)
        self.c = np.count_nonzero(self.question_set3['C'] < 255)
        self.d = np.count_nonzero(self.question_set3['D'] < 255)
        self.e = np.count_nonzero(self.question_set3['E'] < 255)
        self.f = np.count_nonzero(self.question_set3['F'] < 255)
        self.g = np.count_nonzero(self.question_set3['G'] < 255)
        self.h = np.count_nonzero(self.question_set3['H'] < 255)

    def read_img2(self, problem):
        for key in problem.figures:
            img = cv2.imread(problem.figures[key].visualFilename)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            _, threshold = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            threshold[threshold == 0] = 1
            threshold[threshold == 255] = 0
            threshold = threshold.astype(int)

            if ord(key) >= ord("A"):
                self.question_set2[key] = threshold
            else:
                self.answer_set2[key] = threshold

        self.a = np.count_nonzero(self.question_set2['A'])
        self.b = np.count_nonzero(self.question_set2['B'])
        self.c = np.count_nonzero(self.question_set2['C'])

    def method2x2_compare_same(self):
        a, b, c = self.question_set2['A'], self.question_set2['B'], self.question_set2['C']

        if np.count_nonzero(a - b) <= 700:
            for key in self.answer_set2:
                if np.count_nonzero(c - self.answer_set2[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(c - self.answer_set2[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(c - self.answer_set2[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(c - self.answer_set2[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break
        if np.count_nonzero(a - c) <= 700:
            for key in self.answer_set2:
                if np.count_nonzero(b - self.answer_set2[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(b - self.answer_set2[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(b - self.answer_set2[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(b - self.answer_set2[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break

    def method2x2_compare_diff(self):
        a, b, c = self.question_set2['A'], self.question_set2['B'], self.question_set2['C']
        diff_v = a - c
        diff_v[diff_v == -1] = 1
        diff_h = a - b
        diff_h[diff_h == -1] = 1

        for key in self.answer_set2:
            diff_v2 = b - self.answer_set2[key]
            diff_v2[diff_v2 == -1] = 1
            diff_h2 = c - self.answer_set2[key]
            diff_h2[diff_h2 == -1] = 1

            if np.count_nonzero(diff_v - diff_v2) <= 1500 and self.score < 4:
                self.score = 4
                self.answer = key
            if np.count_nonzero(diff_v - diff_v2) <= 1000 and self.score < 6:
                self.score = 6
                self.answer = key
            if np.count_nonzero(diff_v - diff_v2) <= 500 and self.score < 8:
                self.score = 8
                self.answer = key
            if np.count_nonzero(diff_v - diff_v2) <= 100 and self.score < 10:
                self.score = 10
                self.answer = key
                break

            if np.count_nonzero(diff_h - diff_h2) <= 1500 and self.score < 4:
                self.score = 4
                self.answer = key
            if np.count_nonzero(diff_h - diff_h2) <= 1000 and self.score < 6:
                self.score = 6
                self.answer = key
            if np.count_nonzero(diff_h - diff_h2) <= 500 and self.score < 8:
                self.score = 8
                self.answer = key
            if np.count_nonzero(diff_h - diff_h2) <= 100 and self.score < 10:
                self.score = 10
                self.answer = key
                break

    def method2x2_mirror(self):
        a, b, c = self.question_set2['A'], self.question_set2['B'], self.question_set2['C']
        bh, ch, bv, cv = np.flip(b, axis=1), np.flip(c, axis=1), np.flip(b, axis=0), np.flip(c, axis=0)

        if np.count_nonzero(a - bh) <= 800:
            for key in self.answer_set2:
                if np.count_nonzero(ch - self.answer_set2[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(ch - self.answer_set2[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(ch - self.answer_set2[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(ch - self.answer_set2[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break
        if np.count_nonzero(a - cv) <= 800:
            for key in self.answer_set2:
                if np.count_nonzero(bv - self.answer_set2[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(bv - self.answer_set2[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(bv - self.answer_set2[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(bv - self.answer_set2[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break
        if np.count_nonzero(a - ch) <= 1500:
            for key in self.answer_set2:
                if np.count_nonzero(bh - self.answer_set2[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(bh - self.answer_set2[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(bh - self.answer_set2[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(bh - self.answer_set2[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break
        if np.count_nonzero(a - bv) <= 1500:
            for key in self.answer_set2:
                if np.count_nonzero(cv - self.answer_set2[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(cv - self.answer_set2[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(cv - self.answer_set2[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(cv - self.answer_set2[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break

    def method2x2_ratio(self):
        if self.score == 0:
            a, b, c = self.a, self.b, self.c
            ratio = b / a
            best = 100
            for key in self.answer_set2:
                ratio2 = np.count_nonzero(self.answer_set2[key]) / c
                diff = abs(ratio2 - ratio)
                if diff < best:
                    self.answer = key
                    self.score = 1
                    best = diff
