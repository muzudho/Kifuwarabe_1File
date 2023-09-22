import cshogi
# import numpy as np
import random

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

        if not self.board.is_check():
            """自玉に王手がかかっていない時"""

            if (matemove:=self.board.mate_move_in_1ply()):
                """あれば、一手詰めの指し手を取得"""

                print('info score mate 1 pv {}'.format(cshogi.move_to_usi(matemove)))
                return cshogi.move_to_usi(matemove)

        legal_moves = list(self.board.legal_moves)
        """合法手一覧"""

        move = self.choice(legal_moves)
        """指し手を１つ選ぶ"""

        return cshogi.move_to_usi(move)
        """指し手の記法で返却"""

    def choice(self, legal_moves):
        # move = np.random.choice(legal_moves)
        # """乱択"""

        random.shuffle(legal_moves)

        # 取る駒，成るフラグの部分をフィルタして最大値を取る

        move = max(legal_moves, key=lambda x:x & 0b111100000100000000000000)
        """
                                                   ^^^^     ^
                                                   1        2
        1. 取られた駒の種類。0 以外なら何か取った
        2. 1:成り 2:成りでない。 1 なら成った

        最大値だから良いということはないが、同じ局面で、いつも同じ手を選ぶ働きがある

        📖 [1file match（仮）の参考資料２（数行でレートを1300以上上げる）](https://bleu48.hatenablog.com/entry/2023/08/05/122818)
        📖 [cshogi/src/move.hpp](https://github.com/TadaoYamaoka/cshogi/blob/master/src/move.hpp)

        // xxxxxxxx xxxxxxxx xxxxxxxx x1111111  移動先
        // xxxxxxxx xxxxxxxx xx111111 1xxxxxxx  移動元。駒打ちの際には、PieceType + SquareNum - 1
        // xxxxxxxx xxxxxxxx x1xxxxxx xxxxxxxx  1 なら成り
        // xxxxxxxx xxxx1111 xxxxxxxx xxxxxxxx  移動する駒の PieceType 駒打ちの際には使用しない。
        // xxxxxxxx 1111xxxx xxxxxxxx xxxxxxxx  取られた駒の PieceType
        """

        return move

if __name__ == '__main__':
    """コマンドから実行時"""

    kifuwarabe = Kifuwarabe()
    kifuwarabe.usi_loop()
