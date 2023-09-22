import cshogi
# import numpy as np
import random

sente_none=0 # None
sente_pawn=1 # ▲歩
sente_lance=2 # ▲香
sente_knight=3 # ▲桂
sente_silver=4 # ▲銀
sente_bishop=5 # ▲角
sente_rook=6 # ▲飛
sente_gold=7 # ▲金
sente_king=8 # ▲玉
sente_promoted_pawn=9 # ▲と
sente_promoted_lance=10 # ▲杏
sente_promoted_knight=11 # ▲圭
sente_promoted_silver=12 # ▲全
sente_horse=13 # ▲馬
sente_dragon=14 # ▲竜
sente_nouse=15 # 未使用
gote_none=16 # 先手の駒に足すと、後手の駒になる

class KifuwarabesColleague():
    """きふわらべの同僚"""

    def __init__(self, kifuwarabes_subordinate):
        """初期化

        Parameters
        ----------
        kifuwarabes_subordinate
            きふわらべの部下
        """

        self._sense_of_beauty = SenseOfBeauty(
            kifuwarabes_subordinate=kifuwarabes_subordinate,
            kifuwarabes_colleague=self
        )
        """美意識"""

        self._thought = Thought(
            kifuwarabes_subordinate=kifuwarabes_subordinate,
            kifuwarabes_colleague=self
        )
        """思考"""

        self._min_max = MinMax(
            kifuwarabes_subordinate=kifuwarabes_subordinate,
            kifuwarabes_colleague=self
        )
        """ミニマックス戦略"""

    @property
    def sense_of_beauty(self):
        """美意識"""
        return self._sense_of_beauty

    @property
    def thought(self):
        """思考"""
        return self._thought

    @property
    def min_max(self):
        """ミニマックス戦略"""
        return self._min_max

class Kifuwarabe():
    """きふわらべ"""

    def __init__(self):
        """初期化"""

        self._subordinate = KifuwarabesSubordinate()
        """きふわらべの部下"""

        self._colleague = KifuwarabesColleague(
            kifuwarabes_subordinate=self.subordinate)
        """きふわらべの同僚"""

    @property
    def subordinate(self):
        """きふわらべの部下"""
        return self._subordinate

    @property
    def colleague(self):
        """きふわらべの同僚"""
        return self._colleague

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
            self.subordinate.board.reset()

        elif sfen[:5] == 'sfen ':
            """指定局面に変更"""
            self.subordinate.board.set_sfen(sfen[5:])

        for usi_move in usi_moves:
            """棋譜再生"""
            self.subordinate.board.push_usi(usi_move)

    def go(self):
        """思考開始～最善手返却"""

        return self.colleague.thought.do_it()

class KifuwarabesSubordinate():
    """きふわらべの部下"""

    def __init__(self):
        self._board = cshogi.Board()
        """盤"""

        self._materials_value = MaterialsValue()
        """駒の価値"""

    @property
    def board(self):
        """盤"""
        return self._board

    @property
    def materials_value(self):
        """駒の価値"""
        return self._materials_value

class Thought():
    """思考"""

    def __init__(self, kifuwarabes_subordinate, kifuwarabes_colleague):
        """初期化

        Parameters
        ----------
        kifuwarabes_subordinate
            きふわらべの部下
        kifuwarabes_colleague
            きふわらべの同僚
        """

        self._kifuwarabes_subordinate = kifuwarabes_subordinate
        """きふわらべの部下"""

        self._kifuwarabes_colleague = kifuwarabes_colleague
        """きふわらべの同僚"""

    @property
    def kifuwarabes_subordinate(self):
        """きふわらべの部下"""
        return self._kifuwarabes_subordinate

    @property
    def kifuwarabes_colleague(self):
        """きふわらべの同僚"""
        return self._kifuwarabes_colleague

    def do_it(self):
        """それをする"""

        if self.kifuwarabes_subordinate.board.is_game_over():
            """投了局面時"""

            return 'resign'
            """投了"""

        if self.kifuwarabes_subordinate.board.is_nyugyoku():
            """入玉宣言局面時"""

            return 'win'
            """勝利宣言"""

        if not self.kifuwarabes_subordinate.board.is_check():
            """自玉に王手がかかっていない時"""

            if (matemove:=self.kifuwarabes_subordinate.board.mate_move_in_1ply()):
                """あれば、一手詰めの指し手を取得"""

                print('info score mate 1 pv {}'.format(cshogi.move_to_usi(matemove)))
                return cshogi.move_to_usi(matemove)

        legal_moves = list(self.kifuwarabes_subordinate.board.legal_moves)
        """合法手一覧"""

        # move = self.choice_random(legal_moves)
        move = self.choice_min_max(legal_moves)
        """指し手を１つ選ぶ"""

        return cshogi.move_to_usi(move)
        """指し手の記法で返却"""

    def choice_random(self, legal_moves):
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

    def choice_min_max(self, legal_moves):
        """ミニマックス戦略で指し手を選ぶ"""

        max_value = -9999999
        """将来獲得できるであろう、最もよい、最低限の評価値"""

        for move in legal_moves:
            self.kifuwarabes_subordinate.board.push(move)
            """一手指す"""

            checked_value = self.kifuwarabes_colleague.min_max.check_board()
            """あれば、決まりきった盤面評価値"""

            if checked_value is None:
                value = -self.kifuwarabes_colleague.min_max.do_it(depth=2)
                """将来獲得できるであろう、最も良い、最低限の評価値"""

            else:
                value = -checked_value

            if value > max_value:
                max_value = value
                best_move_list = [move]
                """いわゆる、アルファー・アップデート。
                将来獲得できるであろう、最も良い、最低限の評価値が、上がった"""

            elif value == max_value:
                best_move_list.append(move)
                """評価値が等しい指し手を追加"""

            self.kifuwarabes_subordinate.board.pop()
            """一手戻す"""

            bestmove = random.choice(best_move_list)
            """候補手の中からランダムに選ぶ"""

        return bestmove

class MaterialsValue():
    """駒の価値"""

    def __init__(self):
        self._hand = [90,315,405,495,540,855,990,]
        """持ち駒。歩、香、桂、銀、金、角、飛"""

        self._on_board = [
            0,90,315,405,495,855,990,540,0,
            # None、▲歩、▲香、▲桂、▲銀、▲角、▲飛、▲金、▲玉、
            540,540,540,540,945,1395,0,
            # ▲と、▲杏、▲圭、▲全、▲馬、▲竜、未使用、
            0,-90,-315,-405,-495,-855,-990,-540,0,
            # 未使用、▽歩、▽香、▽桂、▽銀、▽角、▽飛、▽金、▽玉、
            -540,-540,-540,-540,-945,-1395,0,0,
            # ▽と、▽杏、▽圭、▽全、▽馬、▽竜、未使用、未使用、
            ]
        """盤上の駒の価値
        📖 [cshogiのサンプルプログラム(MinMax探索)](https://tadaoyamaoka.hatenablog.com/entry/2023/08/13/223655)
        """

    @property
    def hand(self):
        """持ち駒の価値"""
        return self._hand

    @property
    def on_board(self):
        """盤上の駒の価値"""
        return self._on_board

    def eval(self, board):
        """評価"""

        eval_mat = sum(self.on_board[p] for p in board.pieces if p > 0 )
        """盤上の駒の価値"""

        pieces_in_hand = board.pieces_in_hand
        """持ち駒"""

        eval_mat += sum(self.hand[p] * (pieces_in_hand[0][p] - pieces_in_hand[1][p]) for p in range(7) )
        """持ち駒の価値"""

        if board.turn == cshogi.BLACK:
            return eval_mat
        else:
            """後手は評価値の正負を反転"""
            return -eval_mat

class MinMax():
    """ミニマックス戦略"""

    def __init__(self, kifuwarabes_subordinate, kifuwarabes_colleague):
        """初期化

        Parameters
        ----------
        kifuwarabes_subordinate
            きふわらべの部下
        """

        self._kifuwarabes_subordinate = kifuwarabes_subordinate
        """きふわらべの部下"""

        self._kifuwarabes_colleague = kifuwarabes_colleague
        """きふわらべの同僚"""

    @property
    def kifuwarabes_subordinate(self):
        """きふわらべの部下"""
        return self._kifuwarabes_subordinate

    @property
    def kifuwarabes_colleague(self):
        """きふわらべの同僚"""
        return self._kifuwarabes_colleague

    def check_board(self):
        """盤面の評価値"""
        if self.kifuwarabes_subordinate.board.is_game_over():
            return -30000
        if self.kifuwarabes_subordinate.board.is_nyugyoku():
            return 30000

        draw = self.kifuwarabes_subordinate.board.is_draw(16)
        if draw == cshogi.REPETITION_DRAW:
            return 0
        if draw == cshogi.REPETITION_WIN:
            return 30000
        if draw == cshogi.REPETITION_LOSE:
            return -30000
        if draw == cshogi.REPETITION_SUPERIOR:
            return 30000
        if draw == cshogi.REPETITION_INFERIOR:
            return -30000

        """別途、計算が必要"""
        return None

    def do_it(self, depth):
        """それをする

        Parameters
        ----------
        depth
            深さ
        """

        max_value = -9999999
        for move in self.kifuwarabes_subordinate.board.legal_moves:
            self.kifuwarabes_subordinate.board.push(move)
            """一手指す"""

            checked_value = self.check_board()
            """盤面評価値算出"""

            if checked_value is None:
                """別途、計算が必要なケース"""
                if depth > 1:
                    value = -self.do_it(depth=depth - 1)
                    """将来獲得できるであろう、最低限の評価値"""
                else:
                    value = -self.kifuwarabes_subordinate.materials_value.eval(self.kifuwarabes_subordinate.board)
                    """駒割りを、最低限の評価値とする"""

            else:
                value = -checked_value
                """盤面の決まりきった評価値"""

            if value > max_value:
                max_value = value
                """いわゆるアルファー・アップデート。
                自分が将来獲得できるであろう最低限の評価値が、増えた"""

            self.kifuwarabes_subordinate.board.pop()
            """一手戻す"""

        return max_value
        """自分が将来獲得できるであろう、もっとも良い、最低限の評価値"""

class SenseOfBeauty():
    """美意識"""

    def __init__(self, kifuwarabes_subordinate, kifuwarabes_colleague):
        """初期化

        Parameters
        ----------
        kifuwarabes_subordinate
            きふわらべの部下
        kifuwarabes_colleague
            きふわらべの同僚
        """

        self._kifuwarabes_subordinate = kifuwarabes_subordinate
        """きふわらべの部下"""

        self._kifuwarabes_colleague = kifuwarabes_colleague
        """きふわらべの同僚"""

    @property
    def kifuwarabes_subordinate(self):
        """きふわらべの部下"""
        return self._kifuwarabes_subordinate

    @property
    def kifuwarabes_colleague(self):
        """きふわらべの同僚"""
        return self._kifuwarabes_colleague

    def check_ranging_rook(self):
        """振り飛車かどうか調べる
        0: 何でもない
        1: 相居飛車
        2: 先手振り飛車、後手居飛車
        3: 先手居飛車、後手振り飛車
        4: 相振り飛車
        """

        # 局面には２つの飛車がある。
        # 盤上に自分の飛車、相手の飛車があるときのみ発動する

        sente_idx = 0
        gote_idx = 1
        piece_idx = 0 # piece index
        sq_idx = 1 # square index

        rook_pos = []
        for index, piece in enumerate(self.kifuwarabes_subordinate.board.pieces):
            if piece == sente_rook or piece == sente_rook + gote_none:
                rook_pos.append((piece,index))

        if len(rook_pos) == 2:
            if rook_pos[sente_idx][piece_idx] == rook_pos[gote_idx][piece_idx]:
                """先手、後手が分かれていなければ、対象外"""
                pass

            # 先手、後手の順にする
            if rook_pos[gote_idx][piece_idx] == sente_rook and rook_pos[sente_idx][piece_idx] == sente_rook + gote_none:
                temp = rook_pos[gote_idx]
                rook_pos[gote_idx] = rook_pos[sente_idx]
                rook_pos[sente_idx] = temp

            if rook_pos[sente_idx][sq_idx] == 28:
                if rook_pos[gote_idx][sq_idx] == 82:
                    return 1 # 相居飛車
                else:
                    return 3 # 後手振り飛車
            else:
                if rook_pos[gote_idx][sq_idx] == 82:
                    return 2 # 先手振り飛車
                else:
                    return 4 # 相振り飛車

        return 0 # 何でもない

if __name__ == '__main__':
    """コマンドから実行時"""

    kifuwarabe = Kifuwarabe()
    kifuwarabe.usi_loop()
