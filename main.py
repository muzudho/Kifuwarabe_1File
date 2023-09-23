import cshogi
# import numpy as np
import random

# 📖 [_cshogi.pyx](https://github.com/TadaoYamaoka/cshogi/blob/master/cshogi/_cshogi.pyx)

"""
ターン

整数　　意味　　　表記
ーー　　ーーー　　ーーーーーーーーーーー
　０　　先手　　　cshogi.BLACK
　１　　後手　　　cshogi.WHITE

ピースタイプ（PieceType, pt；駒種類）

整数　　意味　　　表記
ーー　　ーーー　　ーーーーーーーーーーー
　０　　未使用
　１　　歩　　　　cshogi.PAWN
　２　　香　　　　cshogi.LANCE
　３　　桂　　　　cshogi.KNIGHT
　４　　銀　　　　cshogi.SILVER
　５　　角　　　　cshogi.BISHOP
　６　　飛　　　　cshogi.ROOK
　７　　金　　　　cshogi.GOLD
　８　　玉　　　　cshogi.KING
　９　　と　　　　cshogi.PROM_PAWN
１０　　杏　　　　cshogi.PROM_LANCE
１１　　圭　　　　cshogi.PROM_KNIGHT
１２　　全　　　　cshogi.PROM_SILVER
１３　　馬　　　　cshogi.PROM_BISHOP
１４　　竜　　　　cshogi.PROM_ROOK
"""

_piece_to_string_array = [
    "　　", # ０．　空升
    "＿歩", # 1
    "＿香", # 2
    "＿桂", # 3
    "＿銀", # 4
    "＿角", # 5
    "＿飛", # 6
    "＿金", # 7
    "＿玉", # 8
    "＿と", # 9
    "＿杏", # 10
    "＿圭", # 11
    "＿全", # 12
    "＿馬", # 13
    "＿竜", # 14
    "１５", # 15. 未使用
    "１６", # 16. 未使用
    "ｖ歩", # 17
    "ｖ香", # 18
    "ｖ桂", # 19
    "ｖ銀", # 20
    "ｖ角", # 21
    "ｖ飛", # 22
    "ｖ金", # 23
    "ｖ玉", # 24
    "ｖと", # 25
    "ｖ杏", # 26
    "ｖ圭", # 27
    "ｖ全", # 28
    "ｖ馬", # 29
    "ｖ竜", # 30
    "３１", # 31. 未使用
    ]

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

    if 0 <= pc and pc < 32:
        return _piece_to_string_array[pc]
    else:
        return f'{pc}' # エラー

_number_of_hand_to_string_list = [
    "　　", #  0
    "　１", #  1
    "　２", #  2
    "　３", #  3
    "　４", #  4
    "　５", #  5
    "　６", #  6
    "　７", #  7
    "　８", #  8
    "　９", #  9
    "１０", # 10
    "１１", # 11
    "１２", # 12
    "１３", # 13
    "１４", # 14
    "１５", # 15
    "１６", # 16
    "１７", # 17
    "１８", # 18
]

def number_of_hand_to_string(number):
    """持ち駒の数の表示文字列"""
    return _number_of_hand_to_string_list[number]

_string_to_piece_table = {
    "　　":0, # 空升
    "＿歩":1,
    "＿香":2,
    "＿桂":3,
    "＿銀":4,
    "＿角":5,
    "＿飛":6,
    "＿金":7,
    "＿玉":8,
    "＿と":9,
    "＿杏":10,
    "＿圭":11,
    "＿全":12,
    "＿馬":13,
    "＿竜":14,
    "１５":15, # 未使用
    "１６":16, # 未使用
    "ｖ歩":17,
    "ｖ香":18,
    "ｖ桂":19,
    "ｖ銀":20,
    "ｖ角":21,
    "ｖ飛":22,
    "ｖ金":23,
    "ｖ玉":24,
    "ｖと":25,
    "ｖ杏":26,
    "ｖ圭":27,
    "ｖ全":28,
    "ｖ馬":29,
    "ｖ竜":30,
    "３１":31, # 未使用
}

def string_to_piece(s):
    """逆関数"""
    if 0 <= s and s < 32:
        return _string_to_piece_table[s]
    else:
        return f'{s}' # エラー

"""
定数　　表記　　　　　　　　　　意味
ーー　　ーーーーーーー　　　　　ーーーーー
　 0　　cshogi.NONE 　　　　　例えば空升
　 1　　cshogi.BPAWN　　　　　▲歩
　 2　　cshogi.BLANCE 　　　　▲香
　 3　　cshogi.BKNIGHT　　　　▲桂
　 4　　cshogi.BSILVER　　　　▲銀
　 5　　cshogi.BBISHOP　　　　▲角
　 6　　cshogi.BROOK　　　　　▲飛
　 7　　cshogi.BGOLD　　　　　▲金
　 8　　cshogi.BKING　　　　　▲玉
　 9　　cshogi.BPROM_PAWN　　▲と
　10　　cshogi.BPROM_LANCE 　▲杏
　11　　cshogi.BPROM_KNIGHT　▲圭
　12　　cshogi.BPROM_SILVER　▲全
　13　　cshogi.BPROM_BISHOP　▲馬
　14　　cshogi.BPROM_ROOK　　▲竜
　15　　　　　　　　　　　　　　未使用
　16　　　　　　　　　　　　　　未使用
　17　　cshogi.PPAWN　　　　　▽歩
　18　　cshogi.PLANCE 　　　　▽香
　19　　cshogi.PKNIGHT　　　　▽桂
　20　　cshogi.PSILVER　　　　▽銀
　21　　cshogi.PBISHOP　　　　▽角
　22　　cshogi.PROOK　　　　　▽飛
　23　　cshogi.PGOLD　　　　　▽金
　24　　cshogi.PKING　　　　　▽玉
　25　　cshogi.PPROM_PAWN　　▽と
　26　　cshogi.PPROM_LANCE 　▽杏
　27　　cshogi.PPROM_KNIGHT　▽圭
　28　　cshogi.PPROM_SILVER　▽全
　29　　cshogi.PPROM_BISHOP　▽馬
　30　　cshogi.PPROM_ROOK　　▽竜
　31　　　　　　　　　　　　　　未使用
"""

_sq_to_jsa_table = [sq // 9 * 10 + 10 + sq % 9 + 1 for sq in range(81)]

def sq_to_jsa(sq):
    """
    cshogi 記法
    　　example: ３四 cshogi.D3、その値は 21 （sq）

    　　９　　８　　７　　６　　５　　４　　３　　２　　１
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜Ａ９｜Ａ８｜Ａ７｜Ａ６｜Ａ５｜Ａ４｜Ａ３｜Ａ２｜Ａ１｜　一
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜Ｂ９｜Ｂ８｜Ｂ７｜Ｂ６｜Ｂ５｜Ｂ４｜Ｂ３｜Ｂ２｜Ｂ１｜　二
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜Ｃ９｜Ｃ８｜Ｃ７｜Ｃ６｜Ｃ５｜Ｃ４｜Ｃ３｜Ｃ２｜Ｃ１｜　三
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜Ｄ９｜Ｄ８｜Ｄ７｜Ｄ６｜Ｄ５｜Ｄ４｜Ｄ３｜Ｄ２｜Ｄ１｜　四
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜Ｅ９｜Ｅ８｜Ｅ７｜Ｅ６｜Ｅ５｜Ｅ４｜Ｅ３｜Ｅ２｜Ｅ１｜　五
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜Ｆ９｜Ｆ８｜Ｆ７｜Ｆ６｜Ｆ５｜Ｆ４｜Ｆ３｜Ｆ２｜Ｆ１｜　六
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜Ｇ９｜Ｇ８｜Ｇ７｜Ｇ６｜Ｇ５｜Ｇ４｜Ｇ３｜Ｇ２｜Ｇ１｜　七
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜Ｈ９｜Ｈ８｜Ｈ７｜Ｈ６｜Ｈ５｜Ｈ４｜Ｈ３｜Ｈ２｜Ｈ１｜　八
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
    ｜Ｉ９｜Ｉ８｜Ｉ７｜Ｉ６｜Ｉ５｜Ｉ４｜Ｉ３｜Ｉ２｜Ｉ１｜　九
    ＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋

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

    return _sq_to_jsa_table[sq]

_jsa_to_sq_table = [(jsa//10-1) * 9 + jsa % 10 - 1 for jsa in range(100)]

def jsa_to_sq(jsa):
    """逆関数
    （ｆｌｏｏｒ（ｊｓａ／１０）ー１）＊９＋（ｊｓａ％１０）ー１"""
    return _jsa_to_sq_table[jsa]

"""
リレーショナル・スクウェア（Relational Square；相対升位置）

　　９　　８　　７　　６　　５　　４　　３　　２　　１
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜６４｜　　｜　　｜　　｜　　｜　　｜　　｜　　｜ー８｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜ー８０｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜５６｜　　｜　　｜　　｜　　｜　　｜　　｜ー７｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜ー７０｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜４８｜　　｜　　｜　　｜　　｜　　｜ー６｜　　　｜　　　｜　　　｜　　　｜　　　｜ー６０｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜４０｜　　｜　　｜　　｜　　｜ー５｜　　　｜　　　｜　　　｜　　　｜ー５０｜　　　｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜３２｜　　｜　　｜　　｜ー４｜　　　｜　　　｜　　　｜ー４０｜　　　｜　　　｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜２４｜　　｜　　｜ー３｜　　　｜　　　｜ー３０｜　　　｜　　　｜　　　｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜　　｜１６｜　７｜ー２｜ー１１｜ー２０｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜　　｜　　｜　８｜ー１｜ー１０｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜７２｜６３｜５４｜４５｜３６｜２７｜１８｜　９｜　★｜　ー９｜ー１８｜ー２７｜ー３６｜ー４５｜ー５４｜ー６３｜ー７２｜　一
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜　　｜　　｜１０｜　１｜　ー８｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　二
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜　　｜２０｜１１｜　２｜　ー７｜ー１６｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　三
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜　　｜３０｜　　｜　　｜　３｜　　　｜　　　｜ー２４｜　　　｜　　　｜　　　｜　　　｜　　　｜　四
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜　　｜４０｜　　｜　　｜　　｜　４｜　　　｜　　　｜　　　｜ー３２｜　　　｜　　　｜　　　｜　　　｜　五
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜　　｜５０｜　　｜　　｜　　｜　　｜　５｜　　　｜　　　｜　　　｜　　　｜ー４０｜　　　｜　　　｜　　　｜　六
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜　　｜６０｜　　｜　　｜　　｜　　｜　　｜　６｜　　　｜　　　｜　　　｜　　　｜　　　｜ー４８｜　　　｜　　　｜　七
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜　　｜７０｜　　｜　　｜　　｜　　｜　　｜　　｜　７｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜ー５６｜　　　｜　八
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋
｜８０｜　　｜　　｜　　｜　　｜　　｜　　｜　　｜　８｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜　　　｜ー６４｜　九
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋ーーー＋

名前と値
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
｜ＮｏｒｔｈＮｏｒｔｈＷｅｓｔ　　７｜　　　　　　　　｜ＮｏｒｔｈＮｏｒｔｈＥａｓｔ　ー１１｜
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
｜ＮｏｒｔｈＷｅｓｔ　　　　　　　８｜Ｎｏｒｔｈ　ー１｜ＮｏｒｔｈＥａｓｔ　　　　　　ー１０｜
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
｜Ｗｅｓｔ　　　　　　　　　　　　９｜★　　　　　　　｜Ｅａｓｔ　　　　　　　　　　　　ー９｜
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
｜ＳｏｕｔｈＷｅｓｔ　　　　　　１０｜Ｓｏｕｔｈ　　１｜ＳｏｕｔｈＥａｓｔ　　　　　　　ー８｜
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
｜ＳｏｕｔｈＳｏｕｔｈＷｅｓｔ　１１｜　　　　　　　　｜ＳｏｕｔｈＳｏｕｔｈＥａｓｔ　　ー７｜
＋ーーーーーーーーーーーーーーーーー＋ーーーーーーーー＋ーーーーーーーーーーーーーーーーーー＋
"""
north_north_east = -11
north_east = -10
east = -9
south_east = -8
south_south_east = -7
north = -1
south = 1
north_north_west = 7
north_west = 8
west = 9
south_west = 10
south_south_west = 11

def non_zero_to_cross(number):
    """非ゼロなら　Ｘ　を表示"""
    if number == 0:
        return "　　"
    else:
        return "　Ｘ"

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
                (bestmove, beta) = self.colleague.thought.do_it()
                alpha = -beta
                print(f'info depth 1 seldepth 1 time 1 nodes 1 score cp {alpha} string x')
                print(f'bestmove {bestmove}', flush=True)

            elif cmd[0] == 'stop':
                """中断"""
                print('bestmove resign' , flush=True)

            elif cmd[0] == 'quit':
                """終了"""
                break

            elif cmd[0] == 'debug':
                """独自拡張。デバッグ"""
                for sq, piece in enumerate(self.subordinate.board.pieces):
                    jsa = sq_to_jsa(sq)
                    print(f'升：{jsa}　駒：{piece_to_string(piece)}　sq：{jsa_to_sq(jsa)}')

                # TODO 適当なマス番号をピックアップ
                origin_sq = random.choice(range(81))
                # TODO 盤上の適当な升をピックアップ
                piece = self.subordinate.board.pieces[origin_sq]
                print(f'[DEBUG] origin_sq:{origin_sq} piece:{piece}')

                if piece == cshogi.NONE:
                    print(f'[DEBUG] miss')
                else:
                    # TODO その駒の利きを取得
                    lst = self.colleague.control.list_by(origin_sq, piece)

                    # TODO その利きを表示
                    print(f'[DEBUG] lst:{lst}')
                    self.colleague.check_board_print.do_it()

            elif cmd[0] == 'beauty':
                """独自拡張。美意識を返す"""

                print(f'ターン：{self.subordinate.board.turn}')

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

                piece_at28 = self.subordinate.board.pieces[cshogi.H2]
                print(f'２八の駒：{piece_to_string(piece_at28)}')

                piece_at82 = self.subordinate.board.pieces[cshogi.B8]
                print(f'８二の駒：{piece_to_string(piece_at82)}')

            elif cmd[0] == 'pos':
                """独自拡張。局面表示"""
                self.colleague.position_print.do_it()


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

        self._kifuwarabes_subordinate = kifuwarabes_subordinate
        """きふわらべの部下"""

        self._position_print = PositionPrint(
            kifuwarabes_subordinate=kifuwarabes_subordinate,
            kifuwarabes_colleague=self
        )
        """局面表示"""

        self._check_board_print = CheckBoardPrint(
            kifuwarabes_subordinate=kifuwarabes_subordinate,
            kifuwarabes_colleague=self
        )
        """チェックボード表示"""

        self._board_value = BoardValue(
            kifuwarabes_subordinate=kifuwarabes_subordinate,
            kifuwarabes_colleague=self
        )
        """盤の決まりきった価値"""

        self._control = Control(
            kifuwarabes_subordinate=kifuwarabes_subordinate,
            kifuwarabes_colleague=self
        )
        """利き"""

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

        self._alpha_beta_pruning = AlphaBetaPruning(
            kifuwarabes_subordinate=kifuwarabes_subordinate,
            kifuwarabes_colleague=self,
            on_eval_on_leaf=self.on_eval_on_leaf
        )
        """探索アルゴリズム　アルファーベーター刈り"""

    @property
    def kifuwarabes_subordinate(self):
        """きふわらべの部下"""
        return self._kifuwarabes_subordinate

    @property
    def check_board_print(self):
        """チェックボード表示"""
        return self._check_board_print

    @property
    def position_print(self):
        """局面表示"""
        return self._position_print

    @property
    def board_value(self):
        """盤の決まりきった価値"""
        return self._board_value

    @property
    def control(self):
        """利き"""
        return self._control

    @property
    def sense_of_beauty(self):
        """美意識"""
        return self._sense_of_beauty

    @property
    def thought(self):
        """思考"""
        return self._thought

    @property
    def alpha_beta_pruning(self):
        """探索アルゴリズム　アルファーベーター刈り"""
        return self._alpha_beta_pruning

    def get_static_exchange_evaluation(self, move):
        """静的駒交換値"""

        # 最後に差した駒の移動先升番号。この升を dst_sq、その駒の種類を dst_pt とでも表記するとする
        dst_sq = MoveHelper.destination(move)
        dst_pt = MoveHelper.piece_type(move)

        # dst_sq に到達できる全ての盤上の駒。これを attacker_list とでも呼ぶとする
        attacker_list = []
        for piece in self.kifuwarabes_subordinate.board.pieces:

            # その駒について、利いている升番号のリスト
            control_list = self.control.list_by(
                origin_sq = dst_sq,
                piece = piece)

            if dst_sq in control_list:
                attacker_list.append(piece)

        # 手番（味方）の駒を入れる friend_queue、 相手番の駒を入れる opponent_queue を作成
        friend_queue = []
        opponent_queue = []

        # dst_pt を opponent_queue へ入れる
        opponent_queue.append(dst_pt)

        for piece in attacker_list:
            if self.kifuwarabes_subordinate.board.turn == cshogi.Black:
                if piece < 16:
                    # attacker_list の中の味方の駒を、価値の安い順に friend_queue へ入れる
                    friend_queue.append(PieceTypeHelper.without_turn(piece))
                else:
                    # attacker_list の中の相手の駒を、価値の安い順に opponent_queue へ入れる
                    opponent_queue.append(PieceTypeHelper.without_turn(piece))
            else:
                if 16 <= piece:
                    friend_queue.append(PieceTypeHelper.without_turn(piece))
                else:
                    opponent_queue.append(PieceTypeHelper.without_turn(piece))

        value = 0

        # opponent_queue、または friend_queue のどちらかのキューが空になるまで、以下を繰り返す
        while 0<len(opponent_queue) and 0<len(friend_queue):
            # 盤面は手番側なので、 opponent_queue の先頭の駒をポップし、その駒の価値を　評価値に加点。
            piece_type = opponent_queue.pop()
            value += self.kifuwarabes_subordinate.materials.piece_type_values[piece_type]

            # TODO 　　friend_queue の先頭の駒をポップし、その駒の価値を　評価値から減点。
            piece_type = friend_queue.pop()
            value -= self.kifuwarabes_subordinate.materials.piece_type_values[piece_type]

        return value

    def on_eval_on_leaf(self, move):
        """末端局面での評価値計算"""

        # 手番から見た駒割評価
        current_beta = self.kifuwarabes_subordinate.materials_value.eval(
            board=self.kifuwarabes_subordinate.board)

        # TODO 駒の取り合いを解消したい。Static Exchange Evaluation
        current_beta += self.get_static_exchange_evaluation(move)

        current_alpha = -current_beta

        ranging_rook = self.sense_of_beauty.check_ranging_rook()

        if ranging_rook == 2:
            # 先手振り飛車
            if cshogi.BLACK == self.kifuwarabes_subordinate.board.turn:
                # 相手が振り飛車やってる
                current_alpha -= 10
            else:
                # 自分が振り飛車やってる
                current_alpha += 10

        elif ranging_rook == 3:
            # 後手振り飛車
            if cshogi.WHITE == self.kifuwarabes_subordinate.board.turn:
                # 相手が振り飛車やってる
                current_alpha -= 10
            else:
                # 自分が振り飛車やってる
                current_alpha += 10

        elif ranging_rook == 1:
            # 相居飛車は、やりたいわけではない
            pass

        elif ranging_rook == 4:
            # 相振り飛車は、やりたいわけではない
            pass

        else:
            # 何でもない
            pass

        return current_alpha

class MaterialsValue():
    """手番から見た駒割評価"""

    def __init__(self):
        # 利き１個 100点換算
        none_value = 0
        pawn_value = 100
        lance_value = 800 // 2
        knight_value = 200
        silver_value = 500
        gold_value = 600
        bishop_value = 1600 // 2
        rook_value = 1600 // 2
        king_value = 0
        promoted_pawn = 600
        promoted_lance = 600
        promoted_knight = 600
        promoted_silver = 600
        horse = 2000 // 2
        dragon = 2000 // 2

        self._hand = [pawn_value, lance_value, knight_value, silver_value, gold_value, bishop_value, rook_value,]
        """持ち駒。歩、香、桂、銀、金、角、飛"""

        self._piece_type_values = [
            none_value, pawn_value, lance_value, knight_value, silver_value, bishop_value, rook_value, gold_value, king_value,
            # None、▲歩、▲香、▲桂、▲銀、▲角、▲飛、▲金、▲玉、
            promoted_pawn, promoted_lance, promoted_knight, promoted_silver, horse, dragon, none_value,
            # ▲と、▲杏、▲圭、▲全、▲馬、▲竜、未使用、
        ]

        self._on_board = [
            none_value, pawn_value, lance_value, knight_value, silver_value, bishop_value, rook_value, gold_value, king_value,
            # None、▲歩、▲香、▲桂、▲銀、▲角、▲飛、▲金、▲玉、
            promoted_pawn, promoted_lance, promoted_knight, promoted_silver, horse, dragon, none_value,
            # ▲と、▲杏、▲圭、▲全、▲馬、▲竜、未使用、
            -none_value, -pawn_value, -lance_value, -knight_value, -silver_value, -bishop_value, -rook_value, -gold_value, -king_value,
            # 未使用、▽歩、▽香、▽桂、▽銀、▽角、▽飛、▽金、▽玉、
            -promoted_pawn, -promoted_lance, -promoted_knight, -promoted_silver, -horse, -dragon, -none_value,
            # ▽と、▽杏、▽圭、▽全、▽馬、▽竜、未使用
            ]
        """盤上の駒の価値
        📖 [cshogiのサンプルプログラム(MinMax探索)](https://tadaoyamaoka.hatenablog.com/entry/2023/08/13/223655)
        """

    @property
    def hand(self):
        """持ち駒の価値"""
        return self._hand

    @property
    def piece_type_values(self):
        """駒の種類別の価値"""
        return self._piece_type_values

    @property
    def on_board(self):
        """盤上の駒の価値"""
        return self._on_board

    def eval(self, board):
        """手番から見た評価"""

        value = sum(self.on_board[pc] for pc in board.pieces if 0 < pc)
        """盤上の駒の価値"""

        pieces_in_hand = board.pieces_in_hand
        """持ち駒"""

        value += sum(self.hand[hand_idx] * (pieces_in_hand[cshogi.BLACK][hand_idx] - pieces_in_hand[cshogi.WHITE][hand_idx]) for hand_idx in range(7) )
        """持ち駒の価値"""

        if board.turn == cshogi.BLACK:
            return value

        else:
            """後手は評価値の正負を反転"""
            return -value

class CheckBoardPrint():
    """チェックボード表示"""

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
        number_board = range(81)

        text = ''

        # 盤
        a = non_zero_to_cross(number_board[cshogi.A1])
        b = non_zero_to_cross(number_board[cshogi.A2])
        c = non_zero_to_cross(number_board[cshogi.A3])
        d = non_zero_to_cross(number_board[cshogi.A4])
        e = non_zero_to_cross(number_board[cshogi.A5])
        f = non_zero_to_cross(number_board[cshogi.A6])
        g = non_zero_to_cross(number_board[cshogi.A7])
        h = non_zero_to_cross(number_board[cshogi.A8])
        i = non_zero_to_cross(number_board[cshogi.A9])
        text += f"""　　９　　８　　７　　６　　５　　４　　３　　２　　１
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　一
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = non_zero_to_cross(number_board[cshogi.B1])
        b = non_zero_to_cross(number_board[cshogi.B2])
        c = non_zero_to_cross(number_board[cshogi.B3])
        d = non_zero_to_cross(number_board[cshogi.B4])
        e = non_zero_to_cross(number_board[cshogi.B5])
        f = non_zero_to_cross(number_board[cshogi.B6])
        g = non_zero_to_cross(number_board[cshogi.B7])
        h = non_zero_to_cross(number_board[cshogi.B8])
        i = non_zero_to_cross(number_board[cshogi.B9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　二
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = non_zero_to_cross(number_board[cshogi.C1])
        b = non_zero_to_cross(number_board[cshogi.C2])
        c = non_zero_to_cross(number_board[cshogi.C3])
        d = non_zero_to_cross(number_board[cshogi.C4])
        e = non_zero_to_cross(number_board[cshogi.C5])
        f = non_zero_to_cross(number_board[cshogi.C6])
        g = non_zero_to_cross(number_board[cshogi.C7])
        h = non_zero_to_cross(number_board[cshogi.C8])
        i = non_zero_to_cross(number_board[cshogi.C9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　三
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = non_zero_to_cross(number_board[cshogi.D1])
        b = non_zero_to_cross(number_board[cshogi.D2])
        c = non_zero_to_cross(number_board[cshogi.D3])
        d = non_zero_to_cross(number_board[cshogi.D4])
        e = non_zero_to_cross(number_board[cshogi.D5])
        f = non_zero_to_cross(number_board[cshogi.D6])
        g = non_zero_to_cross(number_board[cshogi.D7])
        h = non_zero_to_cross(number_board[cshogi.D8])
        i = non_zero_to_cross(number_board[cshogi.D9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　四
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = non_zero_to_cross(number_board[cshogi.E1])
        b = non_zero_to_cross(number_board[cshogi.E2])
        c = non_zero_to_cross(number_board[cshogi.E3])
        d = non_zero_to_cross(number_board[cshogi.E4])
        e = non_zero_to_cross(number_board[cshogi.E5])
        f = non_zero_to_cross(number_board[cshogi.E6])
        g = non_zero_to_cross(number_board[cshogi.E7])
        h = non_zero_to_cross(number_board[cshogi.E8])
        i = non_zero_to_cross(number_board[cshogi.E9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　五
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = non_zero_to_cross(number_board[cshogi.F1])
        b = non_zero_to_cross(number_board[cshogi.F2])
        c = non_zero_to_cross(number_board[cshogi.F3])
        d = non_zero_to_cross(number_board[cshogi.F4])
        e = non_zero_to_cross(number_board[cshogi.F5])
        f = non_zero_to_cross(number_board[cshogi.F6])
        g = non_zero_to_cross(number_board[cshogi.F7])
        h = non_zero_to_cross(number_board[cshogi.F8])
        i = non_zero_to_cross(number_board[cshogi.F9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　六
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = non_zero_to_cross(number_board[cshogi.G1])
        b = non_zero_to_cross(number_board[cshogi.G2])
        c = non_zero_to_cross(number_board[cshogi.G3])
        d = non_zero_to_cross(number_board[cshogi.G4])
        e = non_zero_to_cross(number_board[cshogi.G5])
        f = non_zero_to_cross(number_board[cshogi.G6])
        g = non_zero_to_cross(number_board[cshogi.G7])
        h = non_zero_to_cross(number_board[cshogi.G8])
        i = non_zero_to_cross(number_board[cshogi.G9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　七
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = non_zero_to_cross(number_board[cshogi.H1])
        b = non_zero_to_cross(number_board[cshogi.H2])
        c = non_zero_to_cross(number_board[cshogi.H3])
        d = non_zero_to_cross(number_board[cshogi.H4])
        e = non_zero_to_cross(number_board[cshogi.H5])
        f = non_zero_to_cross(number_board[cshogi.H6])
        g = non_zero_to_cross(number_board[cshogi.H7])
        h = non_zero_to_cross(number_board[cshogi.H8])
        i = non_zero_to_cross(number_board[cshogi.H9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　八
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = non_zero_to_cross(number_board[cshogi.I1])
        b = non_zero_to_cross(number_board[cshogi.I2])
        c = non_zero_to_cross(number_board[cshogi.I3])
        d = non_zero_to_cross(number_board[cshogi.I4])
        e = non_zero_to_cross(number_board[cshogi.I5])
        f = non_zero_to_cross(number_board[cshogi.I6])
        g = non_zero_to_cross(number_board[cshogi.I7])
        h = non_zero_to_cross(number_board[cshogi.I8])
        i = non_zero_to_cross(number_board[cshogi.I9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　九
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        print(text)

class PositionPrint():
    """局面表示"""

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
        board = self.kifuwarabes_subordinate.board

        move_number_str = board.move_number

        if board.turn == cshogi.BLACK:
            turn_str = "black"
        else:
            turn_str = "white"

        text = f'''[{move_number_str} moves / {turn_str}]

'''

        # 後手持ち駒
        a = number_of_hand_to_string(board.pieces_in_hand[cshogi.WHITE][0])
        b = number_of_hand_to_string(board.pieces_in_hand[cshogi.WHITE][1])
        c = number_of_hand_to_string(board.pieces_in_hand[cshogi.WHITE][2])
        d = number_of_hand_to_string(board.pieces_in_hand[cshogi.WHITE][3])
        e = number_of_hand_to_string(board.pieces_in_hand[cshogi.WHITE][4])
        f = number_of_hand_to_string(board.pieces_in_hand[cshogi.WHITE][5])
        g = number_of_hand_to_string(board.pieces_in_hand[cshogi.WHITE][6])

        text += f"""　　歩　　香　　桂　　銀　　金　　角　　飛
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
｜{a}｜{b}｜{c}｜{d}｜{e}｜{f}｜{g}｜
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋

"""

        # 盤
        a = piece_to_string(board.pieces[cshogi.A1])
        b = piece_to_string(board.pieces[cshogi.A2])
        c = piece_to_string(board.pieces[cshogi.A3])
        d = piece_to_string(board.pieces[cshogi.A4])
        e = piece_to_string(board.pieces[cshogi.A5])
        f = piece_to_string(board.pieces[cshogi.A6])
        g = piece_to_string(board.pieces[cshogi.A7])
        h = piece_to_string(board.pieces[cshogi.A8])
        i = piece_to_string(board.pieces[cshogi.A9])
        text += f"""　　９　　８　　７　　６　　５　　４　　３　　２　　１
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　一
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = piece_to_string(board.pieces[cshogi.B1])
        b = piece_to_string(board.pieces[cshogi.B2])
        c = piece_to_string(board.pieces[cshogi.B3])
        d = piece_to_string(board.pieces[cshogi.B4])
        e = piece_to_string(board.pieces[cshogi.B5])
        f = piece_to_string(board.pieces[cshogi.B6])
        g = piece_to_string(board.pieces[cshogi.B7])
        h = piece_to_string(board.pieces[cshogi.B8])
        i = piece_to_string(board.pieces[cshogi.B9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　二
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = piece_to_string(board.pieces[cshogi.C1])
        b = piece_to_string(board.pieces[cshogi.C2])
        c = piece_to_string(board.pieces[cshogi.C3])
        d = piece_to_string(board.pieces[cshogi.C4])
        e = piece_to_string(board.pieces[cshogi.C5])
        f = piece_to_string(board.pieces[cshogi.C6])
        g = piece_to_string(board.pieces[cshogi.C7])
        h = piece_to_string(board.pieces[cshogi.C8])
        i = piece_to_string(board.pieces[cshogi.C9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　三
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = piece_to_string(board.pieces[cshogi.D1])
        b = piece_to_string(board.pieces[cshogi.D2])
        c = piece_to_string(board.pieces[cshogi.D3])
        d = piece_to_string(board.pieces[cshogi.D4])
        e = piece_to_string(board.pieces[cshogi.D5])
        f = piece_to_string(board.pieces[cshogi.D6])
        g = piece_to_string(board.pieces[cshogi.D7])
        h = piece_to_string(board.pieces[cshogi.D8])
        i = piece_to_string(board.pieces[cshogi.D9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　四
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = piece_to_string(board.pieces[cshogi.E1])
        b = piece_to_string(board.pieces[cshogi.E2])
        c = piece_to_string(board.pieces[cshogi.E3])
        d = piece_to_string(board.pieces[cshogi.E4])
        e = piece_to_string(board.pieces[cshogi.E5])
        f = piece_to_string(board.pieces[cshogi.E6])
        g = piece_to_string(board.pieces[cshogi.E7])
        h = piece_to_string(board.pieces[cshogi.E8])
        i = piece_to_string(board.pieces[cshogi.E9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　五
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = piece_to_string(board.pieces[cshogi.F1])
        b = piece_to_string(board.pieces[cshogi.F2])
        c = piece_to_string(board.pieces[cshogi.F3])
        d = piece_to_string(board.pieces[cshogi.F4])
        e = piece_to_string(board.pieces[cshogi.F5])
        f = piece_to_string(board.pieces[cshogi.F6])
        g = piece_to_string(board.pieces[cshogi.F7])
        h = piece_to_string(board.pieces[cshogi.F8])
        i = piece_to_string(board.pieces[cshogi.F9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　六
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = piece_to_string(board.pieces[cshogi.G1])
        b = piece_to_string(board.pieces[cshogi.G2])
        c = piece_to_string(board.pieces[cshogi.G3])
        d = piece_to_string(board.pieces[cshogi.G4])
        e = piece_to_string(board.pieces[cshogi.G5])
        f = piece_to_string(board.pieces[cshogi.G6])
        g = piece_to_string(board.pieces[cshogi.G7])
        h = piece_to_string(board.pieces[cshogi.G8])
        i = piece_to_string(board.pieces[cshogi.G9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　七
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = piece_to_string(board.pieces[cshogi.H1])
        b = piece_to_string(board.pieces[cshogi.H2])
        c = piece_to_string(board.pieces[cshogi.H3])
        d = piece_to_string(board.pieces[cshogi.H4])
        e = piece_to_string(board.pieces[cshogi.H5])
        f = piece_to_string(board.pieces[cshogi.H6])
        g = piece_to_string(board.pieces[cshogi.H7])
        h = piece_to_string(board.pieces[cshogi.H8])
        i = piece_to_string(board.pieces[cshogi.H9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　八
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        a = piece_to_string(board.pieces[cshogi.I1])
        b = piece_to_string(board.pieces[cshogi.I2])
        c = piece_to_string(board.pieces[cshogi.I3])
        d = piece_to_string(board.pieces[cshogi.I4])
        e = piece_to_string(board.pieces[cshogi.I5])
        f = piece_to_string(board.pieces[cshogi.I6])
        g = piece_to_string(board.pieces[cshogi.I7])
        h = piece_to_string(board.pieces[cshogi.I8])
        i = piece_to_string(board.pieces[cshogi.I9])
        text += f"""｜{i}｜{h}｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜　九
＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        # 先手持ち駒
        a = number_of_hand_to_string(board.pieces_in_hand[cshogi.BLACK][0])
        b = number_of_hand_to_string(board.pieces_in_hand[cshogi.BLACK][1])
        c = number_of_hand_to_string(board.pieces_in_hand[cshogi.BLACK][2])
        d = number_of_hand_to_string(board.pieces_in_hand[cshogi.BLACK][3])
        e = number_of_hand_to_string(board.pieces_in_hand[cshogi.BLACK][4])
        f = number_of_hand_to_string(board.pieces_in_hand[cshogi.BLACK][5])
        g = number_of_hand_to_string(board.pieces_in_hand[cshogi.BLACK][6])

        text += f"""
　　　　　　　　飛　　角　　金　　銀　　桂　　香　　歩
　　　　　　＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
　　　　　　｜{g}｜{f}｜{e}｜{d}｜{c}｜{b}｜{a}｜
　　　　　　＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋ーー＋
"""

        print(text)

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
            # 負け
            return -30000

        if self.kifuwarabes_subordinate.board.is_nyugyoku():
            # 入玉宣言勝ち
            return 30000

        draw = self.kifuwarabes_subordinate.board.is_draw(16)

        if draw == cshogi.REPETITION_DRAW:
            # 千日手
            return 0

        if draw == cshogi.REPETITION_WIN:
            # 千日手で勝ち
            return 30000

        if draw == cshogi.REPETITION_LOSE:
            # 千日手で負け
            return -30000

        if draw == cshogi.REPETITION_SUPERIOR:
            # 千日手の上限？？
            return 30000

        if draw == cshogi.REPETITION_INFERIOR:
            # 千日手の下限？？
            return -30000

        """別途、計算が必要"""
        return None

class Control():
    """利き"""

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

        # 長い利きは除く
        self._relative_sq_arrays = [
            #　　　　　　　　＋ーー＋
            #　　０．　　　　｜　　｜
            #　　　　　　　　＋ーー＋
            None,
            #　　　　　　　　＋ーー＋
            #　　　　　　　　｜＊＊｜
            #　　　　　　　　＋ーー＋
            #　　１．　　　　｜＿歩｜
            #　　　　　　　　＋ーー＋
            [north],
            #　　　　　　　　＋ーー＋
            #　　　　　　　　｜＊＊｜
            #　　　　　　　　＋ーー＋
            #　　２．　　　　｜＿香｜
            #　　　　　　　　＋ーー＋
            [north],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜　　｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　　　　｜　　｜
            #　　　　　　　　＋ーー＋
            #　　３．　　　　｜＿桂｜
            #　　　　　　　　＋ーー＋
            [north_north_east, north_north_west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　４．　｜　　｜＿銀｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜　　｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, south_east, north, north_west, south_west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜　　｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　５．　｜　　｜＿角｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜　　｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, south_east, north_west, south_west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　６．　｜＊＊｜＿飛｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [east, north, south, west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　７．　｜＊＊｜＿金｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, east, north, south, north_west, west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　８．　｜＊＊｜＿玉｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, east, south_east, north, south, north_west, west, south_west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　９．　｜＊＊｜＿と｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, east, north, south, north_west, west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　１０．　｜＊＊｜＿杏｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, east, north, south, north_west, west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　１１．　｜＊＊｜＿圭｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, east, north, south, north_west, west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　１２．　｜＊＊｜＿全｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, east, north, south, north_west, west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　１３．　｜＊＊｜＿馬｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, east, south_east, north, south, north_west, west, south_west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　１４．　｜＊＊｜＿竜｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, east, south_east, north, south, north_west, west, south_west],
            #　１５． 未使用
            None,
            #　１６． 未使用
            None,
            #　　　　　　　　＋ーー＋
            #　１７．　　　　｜ｖ歩｜
            #　　　　　　　　＋ーー＋
            #　　　　　　　　｜＊＊｜
            #　　　　　　　　＋ーー＋
            [south],
            #　　　　　　　　＋ーー＋
            #　１８．　　　　｜ｖ香｜
            #　　　　　　　　＋ーー＋
            #　　　　　　　　｜＊＊｜
            #　　　　　　　　＋ーー＋
            [south],
            #　　　　　　　　＋ーー＋
            #　１９．　　　　｜ｖ桂｜
            #　　　　　　　　＋ーー＋
            #　　　　　　　　｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜　　｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [south_south_east, south_south_west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜　　｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　２０．　｜　　｜ｖ銀｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, south_east, south, north_west, south_west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜　　｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　２１．　｜　　｜ｖ角｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜　　｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, south_east, north_west, south_west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　２２．　｜＊＊｜＿飛｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [east, north, south, west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　２３．　｜＊＊｜ｖ金｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [east, south_east, north, south, west, south_east],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　２４．　｜＊＊｜ｖ玉｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, east, south_east, north, south, north_west, west, south_west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　２５．　｜＊＊｜ｖと｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [east, south_east, north, south, west, south_east],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　２６．　｜＊＊｜ｖ杏｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [east, south_east, north, south, west, south_east],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　２７．　｜＊＊｜ｖ圭｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [east, south_east, north, south, west, south_east],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜　　｜＊＊｜　　｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　２８．　｜＊＊｜ｖ全｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [east, south_east, north, south, west, south_east],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　２９．　｜＊＊｜ｖ馬｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, east, south_east, north, south, north_west, west, south_west],
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　３０．　｜＊＊｜ｖ竜｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            #　　　　　｜＊＊｜＊＊｜＊＊｜
            #　　　　　＋ーー＋ーー＋ーー＋
            [north_east, east, south_east, north, south, north_west, west, south_west],
            #　３１． 未使用
            None,
        ]
        """利きを相対位置で設定"""

    @property
    def kifuwarabes_subordinate(self):
        """きふわらべの部下"""
        return self._kifuwarabes_subordinate

    @property
    def kifuwarabes_colleague(self):
        """きふわらべの同僚"""
        return self._kifuwarabes_colleague

    @property
    def relative_sq_arrays(self):
        """配列"""
        return self._relative_sq_arrays

    def list_by(self, origin_sq, piece):
        """利きのリスト"""

        relative_sq_array = self.relative_sq_arrays[piece]

        if relative_sq_array is None:
            return []

        else:
            lst = list(relative_sq_array)

            # TODO 長い利きを考慮
            if piece == cshogi.BLANCE or piece == cshogi.BROOK or piece == cshogi.WROOK or piece == cshogi.BPROM_ROOK or piece == cshogi.WPROM_ROOK:
                #　＿香
                pass

            if piece == cshogi.WLANCE or piece == cshogi.BROOK or piece == cshogi.WROOK:
                #　ｖ香
                pass

            if piece == cshogi.BROOK or piece == cshogi.WROOK or piece == cshogi.BPROM_ROOK or piece == cshogi.WPROM_ROOK:
                #　飛、竜の横
                pass

            if piece == cshogi.BBISHOP or piece == cshogi.WBISHOP or  piece == cshogi.BPROM_BISHOP or piece == cshogi.WPROM_BISHOP:
                #　角、馬
                pass

            # 相対位置を、絶対位置へ変換
            return [sq + origin_sq for sq in lst]



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
            if piece == cshogi.BROOK or piece == cshogi.WROOK:
                rook_pos.append((piece,sq))

        if len(rook_pos) == 2:
            if rook_pos[sente_idx][piece_idx] == rook_pos[gote_idx][piece_idx]:
                """先手、後手が分かれていなければ、対象外"""
                pass

            # 先手、後手の順にする
            if rook_pos[gote_idx][piece_idx] == cshogi.BROOK and rook_pos[sente_idx][piece_idx] == cshogi.WROOK:
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

            return ('resign', 0)
            """投了"""

        if self.kifuwarabes_subordinate.board.is_nyugyoku():
            """入玉宣言局面時"""

            return ('win', 0)
            """勝利宣言"""

        if not self.kifuwarabes_subordinate.board.is_check():
            """自玉に王手がかかっていない時"""

            if (matemove:=self.kifuwarabes_subordinate.board.mate_move_in_1ply()):
                """あれば、一手詰めの指し手を取得"""

                print('info score mate 1 pv {}'.format(cshogi.move_to_usi(matemove)))
                return (cshogi.move_to_usi(matemove), 0)

        # move = self.choice_random(list(self.kifuwarabes_subordinate.board.legal_moves))
        (current_beta, bestmove_list) = self.kifuwarabes_colleague.alpha_beta_pruning.do_it(
            depth=3,
            alpha = -9999999, # 数ある選択肢の中の、評価値の下限。この下限値は、ベータ値いっぱいまで上げたい"""
            beta = 9999999, # 数ある選択肢の中の、評価値の上限。この値を超える選択肢は、相手に必ず妨害されるので選べない
            is_root = True
        )
        """将来獲得できるであろう、最も良い、最低限の評価値"""

        alpha = -current_beta
        bestmove = random.choice(bestmove_list)
        """候補手の中からランダムに選ぶ"""

        return (cshogi.move_to_usi(bestmove), alpha)
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
    #     １．　取られた駒の種類。0 以外なら何か取った
    #     ２．　1:成り 2:成りでない。 1 なら成った
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


class AlphaBetaPruning():
    """探索アルゴリズム　アルファーベーター刈り
    ミニマックス戦略
    実装はネガマックス

    📖 [アルファベータ探索（alpha-beta pruning）やろうぜ（＾～＾）？](https://crieit.net/drafts/60e6206eaf964)
    """

    def __init__(self, kifuwarabes_subordinate, kifuwarabes_colleague, on_eval_on_leaf):
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

        self._on_eval_on_leaf = on_eval_on_leaf
        """末端局面での評価値計算"""

    @property
    def kifuwarabes_subordinate(self):
        """きふわらべの部下"""
        return self._kifuwarabes_subordinate

    @property
    def kifuwarabes_colleague(self):
        """きふわらべの同僚"""
        return self._kifuwarabes_colleague

    @property
    def on_eval_on_leaf(self):
        """末端局面での評価値計算"""
        return self._on_eval_on_leaf

    def do_it(self, depth, alpha, beta, is_root=False):
        """それをする

        Parameters
        ----------
        depth
            深さ
        alpha
            α は、わたし。数ある選択肢の中の、評価値の下限。この下限値は、ベータ値いっぱいまで上げたい
        beta
            β は、あなた。数ある選択肢の中の、評価値の上限。この値を超える選択肢は、相手に必ず妨害されるので選べない
        """

        if is_root:
            best_move_list = []

        beta_cutoff = False

        for move in list(self.kifuwarabes_subordinate.board.legal_moves):

            self.kifuwarabes_subordinate.board.push(move)
            """一手指す"""

            checked_beta = self.kifuwarabes_colleague.board_value.eval()
            """あれば、決まりきった盤面評価値"""

            if checked_beta is None:
                """別途、計算が必要なケース"""

                if depth > 1:
                    (current_beta, _move_list) = self.do_it(
                        depth=depth - 1,
                        alpha=-beta,    # ベーター値は、相手から見ればアルファー値
                        beta=-alpha)    # アルファー値は、相手から見ればベーター値
                    """将来獲得できるであろう、最低限の評価値"""

                    current_alpha = -current_beta

                else:
                    """末端局面評価値"""

                    # どんな手を指したか

                    current_beta = self.on_eval_on_leaf(move)
                    current_alpha = -current_beta

            else:
                current_alpha = -checked_beta
                """盤面の決まりきった評価値"""

            if beta < current_alpha:
                """ベーター・カット"""
                beta_cutoff = True

            elif alpha < current_alpha:
                alpha = current_alpha
                """いわゆるアルファー・アップデート。
                自分が将来獲得できるであろう最低限の評価値が、増えた"""

                if is_root:
                    best_move_list = [move]

            elif is_root and current_alpha == alpha:
                best_move_list.append(move)
                """評価値が等しい指し手を追加"""

            self.kifuwarabes_subordinate.board.pop()
            """一手戻す"""

            if beta_cutoff:
                """これより先の兄弟は、選ばれることはないので打ち切る"""
                break

        if is_root:
            return (alpha, best_move_list)
        else:
            return (alpha, None)
        """自分が将来獲得できるであろう、もっとも良い、最低限の評価値"""

class MoveHelper():
    @staticmethod
    def destination(move):
        """移動先"""
        return move & 0b00000000_00000000_00000000_01111111

    @staticmethod
    def source(move):
        """移動元
        駒打ちの際には、PieceType + SquareNum - 1"""
        return move & 0b00000000_00000000_00111111_10000000 >> 7

    @staticmethod
    def promoted(move):
        """1 なら成り"""
        return move & 0b00000000_00000000_01000000_00000000 >> 14

    @staticmethod
    def piece_type(move):
        """移動する駒の種類。駒打ちの際には使用しない"""
        return move & 0b00000000_00001111_00000000_00000000 >> 16

    @staticmethod
    def captured(move):
        """取られた駒の種類"""
        return move & 0b00000000_11110000_00000000_00000000 >> 20

class PieceHelper():
    """駒ヘルパー"""

    @staticmethod
    def turn_and_piece_type(turn, piece_type):
        return turn * 16 + piece_type

class PieceTypeHelper():
    """駒の種類ヘルパー"""

    @staticmethod
    def without_turn(piece):
        return piece % 16

if __name__ == '__main__':
    """コマンドから実行時"""

    kifuwarabe = Kifuwarabe()
    kifuwarabe.usi_loop()
