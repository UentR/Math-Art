
#include <cstring>

#include <cmath>



using namespace std;

struct Vect{
    int n;
    double *data;

    Vect() : n(0) {
        data = nullptr;
    }

    Vect(int n) : n(n) {
        data = new double[n]();
    }

    Vect(int n, double *arr) : n(n) {
        data = new double[n]();
        memcpy(data, arr, n * sizeof(double));
    }

    Vect(int n, double k) : n(n) {
        data = new double[n]();
        for (int i = 0; i < n; i++) {
            data[i] = k;
        }
    }

    double &operator[](int i) {
        return data[i];
    }

    void Show() {
        cout << "( ";
        for (int i = 0; i < n; i++) {
            cout << data[i] << " ";
        }
        cout << ")";
        cout << endl;
    }

    static Vect Id(int n, int i) {
        Vect res(n, (double)0);
        res[i] = 1;
        return res;
    }

    float norm() {
        float res = 0;
        for (int i = 0; i < n; i++) {
            res += data[i] * data[i];
        }
        return sqrt(res);
    }

    Vect normalize() {
        float norm = this->norm();
        Vect res(n);
        for (int i = 0; i < n; i++) {
            res[i] = data[i] / norm;
        }
        return res;
    }

    int angle() {
        return (atan2(data[1], data[0]) + M_PI/2) * 180 / M_PI;
    }

};


struct Matrix {
    int width, height;
    Vect *data;

    Matrix(int n) : width(n), height(n) {
        data = new Vect[n]{n};
    }
    
    Matrix(int n, int m) : width(m), height(n) {
        data = new Vect[m];
        for (int i = 0; i < n; i++) {
            data[i] = Vect(n, (double)0);
        }
    }

    Matrix(int n, double k) : width(n), height(n) {
        data = new Vect[n];
        for (int i = 0; i < n; i++) {
            data[i] = Vect(n, k);
        }
    }

    Matrix(int n, double *arr) : width(n), height(n) {
        data = new Vect[n];
        for (int i = 0; i < n; i++) {
            data[i] = Vect(n, arr);
        }
    }

    Matrix(int n, int m, double **arr, bool inverse=false) : width(m), height(n) {
        if (inverse && n != m) {
            cout << "Matrix is not square" << endl;
            return;
        }
        data = new Vect[m];
        for (int i = 0; i < n; i++) {
            if (inverse) {
                double *Val = new double[m];
                for (int j = 0; j < m; j++) {
                    Val[j] = arr[j][i];
                }
                data[i] = Vect(m, Val);
            } else {
                data[i] = Vect(m, arr[i]);
            }
        }
    }


    Matrix(int n, int m, Vect (*func)(Vect)) : width(m), height(n) {
        data = new Vect[m]{n};
        for (int i = 0; i < n; i++) {
            data[i] = Vect::Id(m, i);

            data[i] = func(data[i]);
        }
    }

    void set(int i, Vect &v) {
        data[i] = v;
    }

    Vect operator[](int i) {
        return data[i];
    }

    void Show() {
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                cout << data[j][i] << " ";
            }
            cout << endl;
        }
    }

    void apply(double (*func)(double)) {
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                data[j][i] = func(data[j][i]);
            }
        }
    }
};


Vect operator*(Matrix &m, Vect &v) {
    Vect res(v.n);
    for (int i = 0; i < v.n; i++) {
        for (int j = 0; j < v.n; j++) {
            res[i] += m[i][j] * v[j];
        }
    }
    return res;
}

Vect operator+(Vect v1, Vect v2) {
    Vect res(v1.n);
    for (int i = 0; i < v1.n; i++) {
        res[i] = v1[i] + v2[i];
    }
    return res;
}

Vect operator+(Vect &v, double k) {
    Vect res(v.n);
    for (int i = 0; i < v.n; i++) {
        res[i] = v[i] + k;
    }
    return res;
}

Vect operator-(Vect &v1, Vect &v2) {
    Vect res(v1.n);
    for (int i = 0; i < v1.n; i++) {
        res[i] = v1[i] - v2[i];
    }
    return res;
}

Vect operator*(Vect &v, double k) {
    Vect res(v.n);
    for (int i = 0; i < v.n; i++) {
        res[i] = v[i] * k;
    }
    return res;
}

Vect operator*(double k, Vect &v) {
    return v * k;
}

Matrix operator*(Matrix &m1, Matrix &m2) {
    Matrix res(m1.height, m2.width);
    for (int i = 0; i < m1.height; i++) {
        for (int j = 0; j < m2.width; j++) {
            for (int k = 0; k < m1.width; k++) {
                res[i][j] += m1[i][k] * m2[k][j];
            }
        }
    }
    return res;
}

Matrix operator+(Matrix &m1, Matrix &m2) {
    Matrix res(m1.height, m1.width);
    for (int i = 0; i < m1.height; i++) {
        for (int j = 0; j < m1.width; j++) {
            res[i][j] = m1[i][j] + m2[i][j];
        }
    }
    return res;
}

Matrix operator+(Matrix &m, double k) {
    Matrix res(m.height, m.width);
    for (int i = 0; i < m.height; i++) {
        for (int j = 0; j < m.width; j++) {
            res[i][j] = m[i][j] + k;
        }
    }
    return res;
}

Matrix operator*(Matrix &m, double k) {
    Matrix res(m.height, m.width);
    for (int i = 0; i < m.height; i++) {
        for (int j = 0; j < m.width; j++) {
            res[i][j] = m[i][j] * k;
        }
    }
    return res;
}

Matrix operator*(double k, Matrix &m) {
    return m * k;
}

ostream &operator<<(ostream &os, Vect &v) {
    os << "( ";
    for (int i = 0; i < v.n; i++) {
        os << v[i] << " ";
    }
    os << ")";
    return os;
}