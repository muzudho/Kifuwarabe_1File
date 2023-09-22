import cshogi
import numpy as np

class Kifuwarabe():
    """きふわらべ"""

    def __init__(self):
        """初期化"""

        self.board = cshogi.Board()
        """将棋盤"""

    def usi_loop(self):
        """USIループ"""

        while True:

            cmd = input().split(' ', 1)
            """入力"""

            if cmd[0] == 'usi':
                """USIエンジン握手"""
                print('id name Kifuwarabe1File')
                print('usiok', flush=True)

            elif cmd[0] == 'isready':
                """対局準備"""
                print('readyok', flush=True)

            elif cmd[0] == 'position':
                """局面データ解析"""
                pos = cmd[1].split('moves')
                self.position(pos[0].strip(), pos[1].split() if len(pos) > 1 else [])

            elif cmd[0] == 'go':
                """思考開始～最善手返却"""
                print('bestmove ' + self.go(), flush=True)

            elif cmd[0] == 'stop':
                """中断"""
                print('bestmove resign' , flush=True)

            elif cmd[0] == 'quit':
                """終了"""
                break

    def position(self, sfen, usi_moves):
        """局面データ解析"""

        if sfen == 'startpos':
            """平手初期局面に変更"""
            self.board.reset()

        elif sfen[:5] == 'sfen ':
            """指定局面に変更"""
            self.board.set_sfen(sfen[5:])

        for usi_move in usi_moves:
            """棋譜再生"""
            self.board.push_usi(usi_move)

    def go(self):
        """思考開始～最善手返却"""

        thoght = Thought(
            board=self.board
        )
        return thoght.do_it()

class Thought():
    """思考"""

    def __init__(self, board):
        """初期化

        Parameters
        ----------
        board
            将棋盤
        """

        self.board = board
        """将棋盤"""

    def do_it(self):
        """それをする"""

        if self.board.is_game_over():
            """投了局面時"""

            return 'resign'
            """投了"""

        if self.board.is_nyugyoku():
            """入玉宣言局面時"""

            return 'win'
            """勝利宣言"""

        legal_moves = list(self.board.legal_moves)
        """合法手一覧"""

        move = np.random.choice(legal_moves)
        """乱択"""

        return cshogi.move_to_usi(move)
        """指し手の記法で返却"""

if __name__ == '__main__':
    """コマンドから実行時"""

    kifuwarabe = Kifuwarabe()
    kifuwarabe.usi_loop()
