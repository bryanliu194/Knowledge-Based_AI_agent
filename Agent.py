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
        self.question_set = {}
        self.answer_set = {}
        self.methods2x2 = [self.method2x2_compare_same, self.method2x2_mirror, self.method2x2_compare_diff, self.method2x2_ratio]
        self.methods3x3 = [self.method3x3_compare_same, self.method3x3_mirror, self.method3x3_e12, self.method3x3_sum, self.method3x3_add, self.method3x3_add_ac, self.method3x3_e07, self.method3x3_add2, self.method3x3_sub, self.method3x3_common_area, self.method3x3_d06, self.method3x3_diff_ver, self.method3x3_diff_hor, self.method3x3_enlarge]
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
                print(method)
                print(self.score)
                if self.score == 10:
                    break

        answer = self.answer
        print(f'answer {self.answer}')
        print(f'score {self.score}')
        self.__init__()
        return int(answer)

    def method3x3_compare_same(self):
        a, b, c, g = self.question_set['A'], self.question_set['B'], self.question_set['C'], self.question_set['G']
        if np.count_nonzero(a-b) + np.count_nonzero(b-c) < 1200:
            for key in self.answer_set:
                ans = self.answer_set[key]
                if np.count_nonzero(ans - g) == 0:
                    self.answer = key
                    self.score = 10
        # a, b, c, d, e, f, g, h = self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h
        # if a == b and b == c:
        #     for key in self.answer_set:
        #         ans = np.count_nonzero(self.answer_set[key])
        #         if ans == g:
        #             self.answer = key
        #             self.score = 10

    def method3x3_mirror(self):
        a, b, c, g = self.question_set['A'], self.question_set['B'], self.question_set['C'], self.question_set['G']
        bh, ch, gh, bv, cv, gv = np.flip(b, axis=1), np.flip(c, axis=1), np.flip(g, axis=1), np.flip(b, axis=0), np.flip(c, axis=0), np.flip(g, axis=0)
        if np.count_nonzero(a - ch) + np.count_nonzero(b - bh) <= 600:
            for key in self.answer_set:
                diff = np.count_nonzero(gh - self.answer_set[key])
                if diff <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if diff <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if diff <= 600 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if diff <= 300 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break
        # if np.count_nonzero(a - cv) <= 800:
        #     for key in self.answer_set2:
        #         if np.count_nonzero(bv - self.answer_set2[key]) <= 1500 and self.score < 4:
        #             self.score = 4
        #             self.answer = key
        #         if np.count_nonzero(bv - self.answer_set2[key]) <= 1000 and self.score < 6:
        #             self.score = 6
        #             self.answer = key
        #         if np.count_nonzero(bv - self.answer_set2[key]) <= 500 and self.score < 8:
        #             self.score = 8
        #             self.answer = key
        #         if np.count_nonzero(bv - self.answer_set2[key]) <= 100 and self.score < 10:
        #             self.score = 10
        #             self.answer = key
        #             break
        # if np.count_nonzero(a - ch) <= 1500:
        #     for key in self.answer_set2:
        #         if np.count_nonzero(bh - self.answer_set2[key]) <= 1500 and self.score < 4:
        #             self.score = 4
        #             self.answer = key
        #         if np.count_nonzero(bh - self.answer_set2[key]) <= 1000 and self.score < 6:
        #             self.score = 6
        #             self.answer = key
        #         if np.count_nonzero(bh - self.answer_set2[key]) <= 500 and self.score < 8:
        #             self.score = 8
        #             self.answer = key
        #         if np.count_nonzero(bh - self.answer_set2[key]) <= 100 and self.score < 10:
        #             self.score = 10
        #             self.answer = key
        #             break
        # if np.count_nonzero(a - bv) <= 1500:
        #     for key in self.answer_set2:
        #         if np.count_nonzero(cv - self.answer_set2[key]) <= 1500 and self.score < 4:
        #             self.score = 4
        #             self.answer = key
        #         if np.count_nonzero(cv - self.answer_set2[key]) <= 1000 and self.score < 6:
        #             self.score = 6
        #             self.answer = key
        #         if np.count_nonzero(cv - self.answer_set2[key]) <= 500 and self.score < 8:
        #             self.score = 8
        #             self.answer = key
        #         if np.count_nonzero(cv - self.answer_set2[key]) <= 100 and self.score < 10:
        #             self.score = 10
        #             self.answer = key
        #             break

    def method3x3_sum(self):
        a, b, c, d, e, f, g, h = self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h
        best = 10000

        if (d + e + f)*0.95 < a + b + c < (d + e + f)*1.05:
            for key in self.answer_set:
                ans = np.count_nonzero(self.answer_set[key])
                if (g + h + ans) * 0.95 < a + b + c < (g + h + ans) * 1.05 and abs(a + b + c - (g + h + ans)) < best and self.score < 6:
                    best = abs(a + b + c - (g + h + ans))
                    self.answer = key
                    self.score = 6
                if (g + h + ans) * 0.99 < a + b + c < (g + h + ans) * 1.01 and abs(a + b + c - (g + h + ans)) < best and self.score < 8:
                    best = abs(a + b + c - (g + h + ans))
                    self.answer = key
                    self.score = 8
                    break

    def method3x3_add(self):
        a, b, c, g, h = self.question_set['A'], self.question_set['B'], self.question_set['C'], self.question_set['G'], self.question_set['H']
        # a, b, c, g, h = A - 255, B - 255, C - 255, G - 255, H - 255
        best = 10000
        c0 = a + b
        c0 = np.clip(c0, 0, 1)
        if np.count_nonzero(c - c0) < 400:
            for key in self.answer_set:
                ans = self.answer_set[key]
                i = g + h
                i = np.clip(i, 0, 1)
                nonzero = np.count_nonzero(ans - i)
                if nonzero < 400 and nonzero < best:
                    best = nonzero
                    self.answer = key
                    self.score = 10

    def method3x3_add2(self):
        a, b, c, g, h = self.question_set['A'], self.question_set['B'], self.question_set['C'], self.question_set['G'], self.question_set['H']
        # a, b, c, g, h = A - 255, B - 255, C - 255, G - 255, H - 255
        best = 10000
        if np.count_nonzero(a - b - c) < 400:
            for key in self.answer_set:
                ans = self.answer_set[key]
                nonzero = np.count_nonzero(g - h - ans)
                if nonzero < 400 and nonzero < best:
                    best = nonzero
                    self.answer = key
                    self.score = 10

    def method3x3_add_ac(self):
        a, b, c, g, h = self.question_set['A'], self.question_set['B'], self.question_set['C'], self.question_set[
            'G'], self.question_set['H']
        b1 = a + c
        # b1 = np.clip(b1, 0, 1)
        if np.count_nonzero(b - b1) < 800:
            for key in self.answer_set:
                ans = self.answer_set[key]
                h1 = g + ans
                # h1 = np.clip(h1, 0, 1)
                if np.count_nonzero(h - h1) < 1000 and self.score < 8:
                    self.score = 8
                    self.answer = key
                    break
                if np.count_nonzero(h - h1) < 500:
                    self.score = 10
                    self.answer = key
                    break

    def method3x3_e07(self):
        a, d, g, c, f, h = self.question_set['A'], self.question_set['D'], self.question_set['G'], self.question_set[
            'C'], self.question_set['F'], self.question_set['H']
        sum1 = a + d
        sum1 = np.clip(sum1, 0, 1)
        sum2 = d + g
        sum2 = np.clip(sum2, 0, 1)
        if np.count_nonzero(sum1 - sum2) < 200:
            for key in self.answer_set:
                ans = self.answer_set[key]
                sum3 = c + f
                sum3 = np.clip(sum3, 0, 1)
                sum4 = f + ans
                sum4 = np.clip(sum4, 0, 1)
                if np.count_nonzero(sum3 - sum4) < 300 and self.score < 8 and np.count_nonzero(ans - h) > 3000:
                    self.score = 8
                    self.answer = key

    def method3x3_e12(self):
        a, b, c, g, h = self.a, self.b, self.c, self.g, self.h
        if abs(a - b - c) < 100:
            for key in self.answer_set:
                ans = np.count_nonzero(self.answer_set[key])
                if abs(g - h - ans) < 100 and self.score < 8:
                    self.score = 8
                    self.answer = key

    def method3x3_sub(self):
        a, b, c, g, h = self.question_set['A'], self.question_set['B'], self.question_set['C'], self.question_set['G'], self.question_set['H']
        # a, b, c, g, h = A - 255, B - 255, C - 255, G - 255, H - 255
        best = 10000
        sub = a - b
        if np.count_nonzero(sub - c) < 2500:
            for key in self.answer_set:
                ans = self.answer_set[key]
                sub2 = g - h
                sub2[sub2 < 0] = 1
                nonzero = np.count_nonzero(sub2 - ans)
                if nonzero < 2500 and nonzero < best and self.score < 1:
                    best = nonzero
                    self.answer = key
                    self.score = 1
                if nonzero < 1500 and nonzero < best and self.score < 3:
                    best = nonzero
                    self.answer = key
                    self.score = 3
                if nonzero < 500 and nonzero < best and self.score < 5:
                    best = nonzero
                    self.answer = key
                    self.score = 5

    def method3x3_common_area(self):
        a, b, c, g, h = self.question_set['A'], self.question_set['B'], self.question_set['C'], self.question_set[
            'G'], self.question_set['H']
        # a, b, c, g, h = A - 255, B - 255, C - 255, G - 255, H - 255
        best = 100000
        # a = a * 5
        # g = g * 5
        c0 = a + b
        c0[c0 != 2] = 0
        c0[c0 == 2] = 1
        if np.count_nonzero(c0 - c) < 300:
            for key in self.answer_set:
                ans = self.answer_set[key]
                c1 = g + h
                c1[c1 != 2] = 0
                c1[c1 == 2] = 1
                nonzero = np.count_nonzero(c1 - ans)
                if nonzero < 300 and nonzero < best:
                    best = nonzero
                    self.answer = key
                    self.score = 10

    def method3x3_diff_hor(self):
        # a, b, c, d, e, f, g, h = self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h
        # row1 = abs(a - b) + abs(b - c) + abs(a - c)
        # best = 10000
        # for key in self.answer_set:
        #     ans = np.count_nonzero(self.answer_set[key])
        #     row2 = abs(g-h) + abs(h-ans) + abs(g-ans)
        #     if abs(row1-row2) < 100 and abs(row1-row2) < best:
        #         best = abs(row1-row2)
        #         self.answer = key
        #         self.score = 10


        a, b, c, g, h = self.question_set['A'], self.question_set['B'], self.question_set['C'], self.question_set['G'], self.question_set['H']
        if np.count_nonzero(a-b) + np.count_nonzero(b-c) < 1000:
            for key in self.answer_set:
                ans = self.answer_set[key]
                if np.count_nonzero(g - h) + np.count_nonzero(ans-h) < 1000 and self.score < 9:
                    self.answer = key
                    self.score = 9
                if np.count_nonzero(g - h) + np.count_nonzero(ans-h) < 500:
                    self.answer = key
                    self.score = 10
                    break

    def method3x3_d06(self):
        a, d, g, b, e, h, c, f = self.question_set['A'], self.question_set['D'], self.question_set['G'], self.question_set['B'], \
                        self.question_set['E'], self.question_set['H'], self.question_set['C'], self.question_set['F']
        sum1 = a + d + g
        sum2 = b + e + h
        if np.count_nonzero(sum1 - sum2) < 1200:
            for key in self.answer_set:
                ans = self.answer_set[key]
                sum3 = c + f + ans
                if np.count_nonzero(sum1 - sum3) < 700 and self.score < 8:
                    self.answer = key
                    self.score = 8

    def method3x3_diff_ver(self):
        a, c, d, f, g = self.a, self.c, self.d, self.f, self.g

        for key in self.answer_set:
            ans = np.count_nonzero(self.answer_set[key])
            if (c-f)*0.95 < a-d < (c-f)*1.05 or abs(a-d - c+f) < 500 and self.score < 8:
                if (f-ans)*0.95 < d-g < (f-ans)*1.05 or abs(d-g - f+ans) < 500:
                    self.answer = key
                    self.score = 8
            if (c-f)*0.99 < a-d < (c-f)*1.01 or abs(a-d - c+f) < 200:
                if (f-ans)*0.99 < d-g < (f-ans)*1.01 or abs(d-g - f+ans) < 200:
                    self.answer = key
                    self.score = 10

    def method3x3_enlarge(self):
        a, b, c, d, e, f, g, h = self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h

        for key in self.answer_set:
            ans = np.count_nonzero(self.answer_set[key])
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
            threshold[threshold == 0] = 1
            threshold[threshold == 255] = 0
            threshold = threshold.astype(int)

            if ord(key) >= ord("A"):
                self.question_set[key] = threshold
            else:
                self.answer_set[key] = threshold

        self.a = np.count_nonzero(self.question_set['A'])
        self.b = np.count_nonzero(self.question_set['B'])
        self.c = np.count_nonzero(self.question_set['C'])
        self.d = np.count_nonzero(self.question_set['D'])
        self.e = np.count_nonzero(self.question_set['E'])
        self.f = np.count_nonzero(self.question_set['F'])
        self.g = np.count_nonzero(self.question_set['G'])
        self.h = np.count_nonzero(self.question_set['H'])

    def read_img2(self, problem):
        for key in problem.figures:
            img = cv2.imread(problem.figures[key].visualFilename)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            _, threshold = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            threshold[threshold == 0] = 1
            threshold[threshold == 255] = 0
            threshold = threshold.astype(int)

            if ord(key) >= ord("A"):
                self.question_set[key] = threshold
            else:
                self.answer_set[key] = threshold

        self.a = np.count_nonzero(self.question_set['A'])
        self.b = np.count_nonzero(self.question_set['B'])
        self.c = np.count_nonzero(self.question_set['C'])

    def method2x2_compare_same(self):
        a, b, c = self.question_set['A'], self.question_set['B'], self.question_set['C']

        if np.count_nonzero(a - b) <= 700:
            for key in self.answer_set:
                if np.count_nonzero(c - self.answer_set[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(c - self.answer_set[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(c - self.answer_set[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(c - self.answer_set[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break
        if np.count_nonzero(a - c) <= 700:
            for key in self.answer_set:
                if np.count_nonzero(b - self.answer_set[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(b - self.answer_set[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(b - self.answer_set[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(b - self.answer_set[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break

    def method2x2_compare_diff(self):
        a, b, c = self.question_set['A'], self.question_set['B'], self.question_set['C']
        diff_v = a - c
        diff_v[diff_v == -1] = 1
        diff_h = a - b
        diff_h[diff_h == -1] = 1

        for key in self.answer_set:
            diff_v2 = b - self.answer_set[key]
            diff_v2[diff_v2 == -1] = 1
            diff_h2 = c - self.answer_set[key]
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
        a, b, c = self.question_set['A'], self.question_set['B'], self.question_set['C']
        bh, ch, bv, cv = np.flip(b, axis=1), np.flip(c, axis=1), np.flip(b, axis=0), np.flip(c, axis=0)

        if np.count_nonzero(a - bh) <= 800:
            for key in self.answer_set:
                if np.count_nonzero(ch - self.answer_set[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(ch - self.answer_set[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(ch - self.answer_set[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(ch - self.answer_set[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break
        if np.count_nonzero(a - cv) <= 800:
            for key in self.answer_set:
                if np.count_nonzero(bv - self.answer_set[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(bv - self.answer_set[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(bv - self.answer_set[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(bv - self.answer_set[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break
        if np.count_nonzero(a - ch) <= 1500:
            for key in self.answer_set:
                if np.count_nonzero(bh - self.answer_set[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(bh - self.answer_set[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(bh - self.answer_set[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(bh - self.answer_set[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break
        if np.count_nonzero(a - bv) <= 1500:
            for key in self.answer_set:
                if np.count_nonzero(cv - self.answer_set[key]) <= 1500 and self.score < 4:
                    self.score = 4
                    self.answer = key
                if np.count_nonzero(cv - self.answer_set[key]) <= 1000 and self.score < 6:
                    self.score = 6
                    self.answer = key
                if np.count_nonzero(cv - self.answer_set[key]) <= 500 and self.score < 8:
                    self.score = 8
                    self.answer = key
                if np.count_nonzero(cv - self.answer_set[key]) <= 100 and self.score < 10:
                    self.score = 10
                    self.answer = key
                    break

    def method2x2_ratio(self):
        if self.score == 0:
            a, b, c = self.a, self.b, self.c
            ratio = b / a
            best = 100
            for key in self.answer_set:
                ratio2 = np.count_nonzero(self.answer_set[key]) / c
                diff = abs(ratio2 - ratio)
                if diff < best:
                    self.answer = key
                    self.score = 1
                    best = diff
