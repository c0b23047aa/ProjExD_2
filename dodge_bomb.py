import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (+5, 0), 
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横, 縦）/画面内：True, 画面外：False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表示し，
    泣いているこうかとん画像を貼り付ける関数
    引数：スクリーンSurface
    戻り値：なし
    """
    go_img = pg.Surface((WIDTH, HEIGHT))  #黒半透明画像Surface
    pg.draw.rect(go_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    go_img.set_alpha(200)  #画像の透明度設定
    go_rct = go_img.get_rect()
    go_rct.topleft = 0, 0
    ks_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    fonto = pg.font.Font(None, 80)  #フォントサイズの設定
    txt = fonto.render("Game Over", True, (255, 255, 255))
    #テキストの文字列と色の設定
    screen.blit(go_img, go_rct)
    screen.blit(ks_img, [WIDTH/2-200, HEIGHT/2])
    screen.blit(ks_img, [WIDTH/2+200, HEIGHT/2])
    screen.blit(txt, [WIDTH/2-130, HEIGHT/2])
    #中心座標を基準にblitする
    pg.display.update()
    time.sleep(5)  #5秒間表示


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の10段階程度の大きさ，加速度を準備する関数
    引数：なし
    戻り値：10段階程度の加速度，大きさのリスト
    """
    bb_accs = [a for a in range(1, 11)]  #加速度のリスト
    bb_imgs = []  #拡大爆弾Surfaceのリスト（空）
    for r in range(1, 11):
        #for文で10段階の大きさの爆弾Surfaceを追加する
        bb_img = pg.Surface((20*r, 20*r)) 
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  #爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  #爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))  #四隅の黒を消す
    bb_rct = bb_img.get_rect()  #爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)  #ゲームオーバー
            return
        bb_imgs, bb_accs = init_bb_imgs()
        #10段階程度の大きさ，加速度のリストを呼び出す
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        #tmrの値に応じて，リストから適切な要素を選択する
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        #こうかとんが画面外なら，元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)  #爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  #横にはみ出る
            vx *= -1
        if not tate:  #縦にはみ出る
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
