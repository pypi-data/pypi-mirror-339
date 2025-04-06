def tambah(*args: int) -> int:
    """
    Menjumlahkan semua argumen yang diberikan

    parameter:
    args : int : argumen yang akan dijumlahkan

    return:
    int : hasil penjumlahan dari semua argumen
    """
    if all(isinstance(arg, int) for arg in args):
        hasil = 0
        for arg in args:
            hasil += arg
        return hasil
    else:
        raise TypeError("Argumen harus berupa integer")

def kurang(*args: int) -> int:
    """
    Mengurangkan semua argumen yang diberikan

    parameter:
    args : int : argumen yang akan dikurangkan

    return:
    int : hasil pengurangan dari semua argumen
    """
    if all(isinstance(arg, int) for arg in args):
        hasil = args[0]
        for arg in args[1:]:
            hasil -= arg
        return hasil
    else:
        raise TypeError("Argumen harus berupa integer")

def kali(*args: int) -> int:
    """
    Mengalikan semua argumen yang diberikan

    parameter:
    args : int : argumen yang akan dikalikan

    return:
    int : hasil perkalian dari semua argumen
    """
    if all(isinstance(arg, int) for arg in args):
        hasil = 1
        for arg in args:
            hasil *= arg
        return hasil
    else:
        raise TypeError("Argumen harus berupa integer")

def bagi(*args: int) -> int:
    """
    Membagi semua argumen yang diberikan

    parameter:
    args : int : argumen yang akan dibagi

    return:
    int : hasil pembagian dari semua argumen
    """
    if all(isinstance(arg, int) for arg in args):
        try:
            hasil = args[0]
            for arg in args[1:]:
                hasil /= arg
            return hasil
        except ZeroDivisionError:
            print("Tidak bisa dibagi dengan 0")
    else:
        raise TypeError("Argumen harus berupa integer")

def pangkat(*args: int) -> int:
    """
    Mempangkatkan semua argumen yang diberikan

    parameter:
    args : int : argumen yang akan dipangkatkan

    return:
    int : hasil pemangkatan dari semua argumen
    """
    if all(isinstance(arg, int) for arg in args):
        hasil = args[0]
        for arg in args[1:]:
            hasil **= arg
        return hasil
    else:
        raise TypeError("Argumen harus berupa integer")


def faktorial(n: int) -> int:
    """
    Menghitung faktorial dari argumen yang diberikan (n)

    parameter:
    n : int : angka yang akan dihitung faktorialnya

    return:
    int : hasil faktorial dari n

    """

    if isinstance(n, int): 
        hasil = 1
        for i in range(1, n + 1) :
            hasil *= i
        return hasil
    else:
        raise TypeError("Argumen harus berupa integer")
        
def nilai_terkecil(arr: list) -> int:
    """
    Mengembalikan nilai terkecil dari list yang diberikan

    parameter:
    arr : list : list yang akan dicari nilai terkecilnya

    return:
    int : nilai terkecil dari list yang diberikan

    """

    if isinstance(arr, list):
        left = arr[0]
        for i in range(1, len(arr)):
            if arr[i] < left:
                left = arr[i]
        return left
    else:
        raise TypeError("Argumen harus berupa list")

def nilai_terbesar(arr: list) -> int:
    """
    Mengembalikan nilai terbesar dari list yang diberikan

    parameter:
    arr : list : list yang akan dicari nilai terbesarnya

    return:
    int : nilai terbesar dari list yang diberikan

    """

    if isinstance(arr, list):
        left = arr[0]
        for i in range(1, len(arr)):
            if arr[i] > left:
                left = arr[i]
        return left
    else:
        raise TypeError("Argumen harus berupa list")

def fibbonaci(n: int) -> int:
    """
    Menghitung deret fibonacci ke-n

    parameter:
    n : int : angka ke-n dari deret fibonacci

    return:
    int : angka ke-n dari deret fibonacci

    """

    if isinstance(n, int):
        if n <= 1:
            return n
        a, b = 0, 1  
        for _ in range(2, n + 1):
            a, b = b, a + b 
        return b
    else:  
        raise TypeError("Argumen harus berupa integer")

def rata(arr: list) -> int:

    """
    Fungsi untuk menghitung rata-rata

    parameter : 
    arr : list : kumpulan angka dari list

    return :
    int : berupa hasil dari perataan nilai di dalam list
    """

    if isinstance(arr, list):
        hasil = 0
        for i in arr:
            hasil += i
        
        fix = hasil / len(arr)
        return fix
    else:
        raise TypeError("Argument harus berupa list")