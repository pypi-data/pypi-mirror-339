class console:
    @staticmethod
    def log(*texts, sep=' ', end='\n'):
        for i in range(len(texts)):
            print(texts[i], end=sep if i != len(texts) - 1 else '')
        print(end, end='')

    @staticmethod
    def warn(*texts, sep=' ', end='\n'):
        print("⚠️  | ", end='')
        console.log(*texts, sep=sep, end=end)

    @staticmethod
    def error(*texts, sep=' ', end='\n'):
        print("❌  | ", end='')
        console.log(*texts, sep=sep, end=end)

    @staticmethod
    def success(*texts, sep=' ', end='\n'):
        print("✅  | ", end='')
        console.log(*texts, sep=sep, end=end)
