import cshogi
# import numpy as np
import random

def piece_to_string(pc):
    """
    ピース（Piece, pc；駒番号）

    　０　空升
    １６　未使用

    　　　　　先手　　　後手
    　　　　ーーー　　ーーー
    　　歩　　　１　　　１７
    　　香　　　２　　　１８
    　　桂　　　３　　　１９
    　　銀　　　４　　　２０
    　　角　　　５　　　２１
    　　飛　　　６　　　２２
    　　金　　　７　　　２３
    　　玉　　　８　　　２４
    　　と　　　９　　　２５
    　　杏　　１０　　　２６
    　　圭　　１１　　　２７
    　　全　　１２　　　２８
    　　馬　　１３　　　２９
    　　竜　　１４　　　３０
    未使用　　１５　　　３１
    """

    if pc == 0:
        return "　　" # 空升
    elif pc == 1:
        return "＿歩"
    elif pc == 2:
        return "＿香"
    elif pc == 3:
        return "＿桂"
    elif pc == 4:
        return "＿銀"
    elif pc == 5:
        return "＿角"
    elif pc == 6:
        return "＿飛"
    elif pc == 7:
        return "＿金"
    elif pc == 8:
        return "＿玉"
    elif pc == 9:
        return "＿と"
    elif pc == 10:
        return "＿杏"
    elif pc == 11:
        return "＿圭"
    elif pc == 12:
        return "＿全"
    elif pc == 13:
        return "＿馬"
    elif pc == 14:
        return "＿竜"
    elif pc == 15:
        return "１５" # 未使用
    elif pc == 16:
        return "１６" # 未使用
    elif pc == 17:
        return "ｖ歩"
    elif pc == 18:
        return "ｖ香"
    elif pc == 19:
        return "ｖ桂"
    elif pc == 20:
        return "ｖ銀"
    elif pc == 21:
        return "ｖ角"
    elif pc == 22:
        return "ｖ飛"
    elif pc == 23:
        return "ｖ金"
    elif pc == 24:
        return "ｖ玉"
    elif pc == 25:
        return "ｖと"
    elif pc == 26:
        return "ｖ杏"
    elif pc == 27:
        return "ｖ圭"
    elif pc == 28:
        return "ｖ全"
    elif pc == 29:
        return "ｖ馬"
    elif pc == 30:
        return "ｖ竜"
    elif pc == 31:
        return "３１" # 未使用
    else:
        return f'{pc}' # エラー

def string_to_piece(s):
    """逆関数"""
    if s == "　　": # 空升
        return 0
    elif s == "＿歩":
        return 1
    elif s == "＿香":
        return 2
    elif s == "＿桂":
        return 3
    elif s == "＿銀":
        return 4
    elif s == "＿角":
        return 5
    elif s == "＿飛":
        return 6
    elif s == "＿金":
        return 7
    elif s == "＿玉":
        return 8
    elif s == "＿と":
        return 9
    elif s == "＿杏":
        return 10
    elif s == "＿圭":
        return 11
    elif s == "＿全":
        return 12
    elif s == "＿馬":
        return 13
    elif s == "＿竜":
        return 14
    elif s == "１５": # 未使用
        return 15
    elif s == "１６": # 未使用
        return 16
    elif s == "ｖ歩":
        return 17
    elif s == "ｖ香":
        return 18
    elif s == "ｖ桂":
        return 19
    elif s == "ｖ銀":
        return 20
    elif s == "ｖ角":
        return 21
    elif s == "ｖ飛":
        return 22
    elif s == "ｖ金":
        return 23
    elif s == "ｖ玉":
        return 24
    elif s == "ｖと":
        return 25
    elif s == "ｖ杏":
        return 26
    elif s == "ｖ圭":
        return 27
    elif s == "ｖ全":
        return 28
    elif s == "ｖ馬":
        return 29
    elif s == "ｖ竜":
        return 30
    elif s == "３１": # 未使用
        return 31
    else:
        return f'{s}' # エラー

sente_none=0 # None 例えば空升
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

def sq_to_jsa(sq):
    """
    スクウェア（Square, sq；升番号）

    　　９　　８　　７　　６　　５　　４　　３　　２　　１
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜７２｜６３｜５４｜４５｜３６｜２７｜１８｜　９｜　０｜　一
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜７３｜６４｜５５｜４６｜３７｜２８｜１９｜１０｜　１｜　二
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜７４｜６５｜５６｜４７｜３８｜２９｜２０｜１１｜　２｜　三
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜７５｜６６｜５７｜４８｜３９｜３０｜２１｜１２｜　３｜　四
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜７６｜６７｜５８｜４９｜４０｜３１｜２２｜１３｜　４｜　五
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜７７｜６８｜５９｜５０｜４１｜３２｜２３｜１４｜　５｜　六
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜７８｜６９｜６０｜５１｜４２｜３３｜２４｜１５｜　６｜　七
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜７９｜７０｜６１｜５２｜４３｜３４｜２５｜１６｜　７｜　八
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜８０｜７１｜６２｜５３｜４４｜３５｜２６｜１７｜　８｜　九
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋

    ジェイ・エス・エー（ＪＳＡ；日本将棋連盟）方式
    　　ｆｌｏｏｒ（ｓｑ／９）＊１０＋１０＋（ｓｑ％９）＋１

    　　９　　８　　７　　６　　５　　４　　３　　２　　１
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜９１｜８１｜７１｜６１｜５１｜４１｜３１｜２１｜１１｜　一
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜９２｜８２｜７２｜６２｜５２｜４２｜３２｜２２｜１２｜　二
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜９３｜８３｜７３｜６３｜５３｜４３｜３３｜２３｜１３｜　三
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜９４｜８４｜７４｜６４｜５４｜４４｜３４｜２４｜１４｜　四
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜９５｜８５｜７５｜６５｜５５｜４５｜３５｜２５｜１５｜　五
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜９６｜８６｜７６｜６６｜５６｜４６｜３６｜２６｜１６｜　六
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜９７｜８７｜７７｜６７｜５７｜４７｜３７｜２７｜１７｜　七
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜９８｜８８｜７８｜６８｜５８｜４８｜３８｜２８｜１８｜　八
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜９９｜８９｜７９｜６９｜５９｜４９｜３９｜２９｜１９｜　九
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    """
    return sq // 9 * 10 + 10 + sq % 9 + 1

def jsa_to_sq(jsa):
    """逆関数
    （ｆｌｏｏｒ（ｊｓａ／１０）ー１）＊９＋（ｊｓａ％１０）ー１"""
    return (jsa//10-1) * 9 + jsa % 10 - 1

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

            elif cmd[0] == 'debug':
                """独自拡張。デバッグ"""
                for sq, piece in enumerate( self.subordinate.board.pieces):
                    jsa = sq_to_jsa(sq)
                    print(f'升：{jsa}　駒：{piece_to_string(piece)}　sq：{jsa_to_sq(jsa)}')

            elif cmd[0] == 'beauty':
                """独自拡張。美意識を返す"""
                ranging_rook = self.colleague.sense_of_beauty.check_ranging_rook()
                if ranging_rook == 0:
                    print(f'beauty 何でもない')
                elif ranging_rook == 1:
                    print(f'beauty 相居飛車')
                elif ranging_rook == 2:
                    print(f'beauty 先手振り飛車')
                elif ranging_rook == 3:
                    print(f'beauty 後手振り飛車')
                elif ranging_rook == 4:
                    print(f'beauty 相振り飛車')

                piece_at28 = self.subordinate.board.pieces[jsa_to_sq(28)]
                print(f'２八の駒：{piece_to_string(piece_at28)}')

                piece_at82 = self.subordinate.board.pieces[jsa_to_sq(82)]
                print(f'８二の駒：{piece_to_string(piece_at82)}')


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
        """初期化"""

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

class KifuwarabesColleague():
    """きふわらべの同僚"""

    def __init__(self, kifuwarabes_subordinate):
        """初期化

        Parameters
        ----------
        kifuwarabes_subordinate
            きふわらべの部下
        """

        self._board_value = BoardValue(
            kifuwarabes_subordinate=kifuwarabes_subordinate,
            kifuwarabes_colleague=self
        )
        """盤の決まりきった価値"""

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
    def board_value(self):
        """盤の決まりきった価値"""
        return self._board_value

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

class BoardValue():
    """盤の決まりきった価値"""

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

    def eval(self):
        """評価"""
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
        for sq, piece in enumerate(self.kifuwarabes_subordinate.board.pieces):
            if piece == sente_rook or piece == sente_rook + gote_none:
                rook_pos.append((piece,sq))

        if len(rook_pos) == 2:
            if rook_pos[sente_idx][piece_idx] == rook_pos[gote_idx][piece_idx]:
                """先手、後手が分かれていなければ、対象外"""
                pass

            # 先手、後手の順にする
            if rook_pos[gote_idx][piece_idx] == sente_rook and rook_pos[sente_idx][piece_idx] == sente_rook + gote_none:
                temp = rook_pos[gote_idx]
                rook_pos[gote_idx] = rook_pos[sente_idx]
                rook_pos[sente_idx] = temp

            if rook_pos[sente_idx][sq_idx] == jsa_to_sq(28):
                if rook_pos[gote_idx][sq_idx] == jsa_to_sq(82):
                    return 1 # 相居飛車
                else:
                    return 3 # 後手振り飛車
            else:
                if rook_pos[gote_idx][sq_idx] == jsa_to_sq(82):
                    return 2 # 先手振り飛車
                else:
                    return 4 # 相振り飛車

        return 0 # 何でもない

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

    # def choice_random(self, legal_moves):
    #     # move = np.random.choice(legal_moves)
    #     # """乱択"""
    # 
    #     random.shuffle(legal_moves)
    # 
    #     # 取る駒，成るフラグの部分をフィルタして最大値を取る
    # 
    #     move = max(legal_moves, key=lambda x:x & 0b111100000100000000000000)
    #     """
    #                                                ^^^^     ^
    #                                                1        2
    #     1. 取られた駒の種類。0 以外なら何か取った
    #     2. 1:成り 2:成りでない。 1 なら成った
    # 
    #     最大値だから良いということはないが、同じ局面で、いつも同じ手を選ぶ働きがある
    # 
    #     📖 [1file match（仮）の参考資料２（数行でレートを1300以上上げる）](https://bleu48.hatenablog.com/entry/2023/08/05/122818)
    #     📖 [cshogi/src/move.hpp](https://github.com/TadaoYamaoka/cshogi/blob/master/src/move.hpp)
    # 
    #     // xxxxxxxx xxxxxxxx xxxxxxxx x1111111  移動先
    #     // xxxxxxxx xxxxxxxx xx111111 1xxxxxxx  移動元。駒打ちの際には、PieceType + SquareNum - 1
    #     // xxxxxxxx xxxxxxxx x1xxxxxx xxxxxxxx  1 なら成り
    #     // xxxxxxxx xxxx1111 xxxxxxxx xxxxxxxx  移動する駒の PieceType 駒打ちの際には使用しない。
    #     // xxxxxxxx 1111xxxx xxxxxxxx xxxxxxxx  取られた駒の PieceType
    #     """
    # 
    #     return move

    def choice_min_max(self, legal_moves):
        """ミニマックス戦略で指し手を選ぶ"""

        max_value = -9999999
        """将来獲得できるであろう、最もよい、最低限の評価値"""

        for move in legal_moves:
            self.kifuwarabes_subordinate.board.push(move)
            """一手指す"""

            checked_value = self.kifuwarabes_colleague.board_value.eval()
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

            checked_value = self.kifuwarabes_colleague.board_value.eval()
            """盤面評価値算出"""

            if checked_value is None:
                """別途、計算が必要なケース"""

                if depth > 1:
                    value = -self.do_it(depth=depth - 1)
                    """将来獲得できるであろう、最低限の評価値"""
                else:
                    """末端局面評価値"""

                    value = -self.kifuwarabes_subordinate.materials_value.eval(self.kifuwarabes_subordinate.board)
                    """駒割りを、最低限の評価値とする"""

                    ranging_rook = self.kifuwarabes_colleague.sense_of_beauty.check_ranging_rook()
                    if ranging_rook == 0:
                        # 何でもない
                        pass

                    elif ranging_rook == 1:
                        # 相居飛車は避けたい。 -8000点したれ
                        value -= 8000

                    elif ranging_rook == 4:
                        # 相振り飛車は、やりたいわけではない。 -2000点したれ
                        value -= 2000

                    else:
                        # 対抗系なら、居飛車側持つかもしれないけど、いいや
                        value += 5000
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

if __name__ == '__main__':
    """コマンドから実行時"""

    kifuwarabe = Kifuwarabe()
    kifuwarabe.usi_loop()
