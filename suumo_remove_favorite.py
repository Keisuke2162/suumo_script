from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# ChromeDriverのパスを指定
service = Service("/usr/local/bin/chromedriver")  # 実際のパスを記載

# ブラウザオプション設定
options = Options()
options.add_argument("--start-maximized")

# WebDriver作成
driver = webdriver.Chrome(service=service, options=options)

try:
    # suumoのログインページ
    driver.get("https://point.recruit.co.jp/member/OIDCLogin/?response_type=code&scope=openid+r_email+r_profile+r_address+r_phone+r_ml_magzn&sc_ap=null&redirect_uri=https%3A%2F%2Fsuumo.jp%2Fjj%2Fcommon%2Fcommon%2FJJ901FK101%2Flogin&state=eyJhdXRoQ2xpZW50SWQiOm51bGwsImhhbmt5b0tleSI6bnVsbCwidmZjVG9rZW4iOiI5NDRjZGMxOTE5ZDBmZDkxNWMxNDk2NmU5MzdhYzQyYyJ9&client_id=6affbce57a0c50a2903984242cad22b2619a5ae452be1b41555da255f2714e54&sc_vid=13D6AF33F5F775CA-16BBC39F2C7D0DDF")  # 実際のURLに置き換え

    # ログイン処理
    username = driver.find_element(By.ID, "mainEmail")  # 適切なIDやセレクターを使用
    password = driver.find_element(By.ID, "passwordText")
    login_button = driver.find_element(By.ID, "sbmbtn")

    username.send_keys("{email}")
    password.send_keys("{password}")
    login_button.click()
    time.sleep(3)

    # お気に入りページに移動
    driver.get("https://suumo.jp/jj/common/service/JJ901FM201/?ar=030&cts=01")  # 実際のURLに置き換え
    time.sleep(2)

    # お気に入り削除ボタンを一括でクリック
    while True:
        # 削除ボタンを探す
        delete_buttons = driver.find_elements(By.CLASS_NAME, "cassette_delete")  # 実際のクラス名に置き換え

        if not delete_buttons:
            print("削除ボタンが見つかりません、終了。")
            break

        for button in delete_buttons:
            ActionChains(driver).move_to_element(button).click().perform()  # ボタンクリック
            time.sleep(1)

            # 削除確認ボタンの存在確認とクリック
            try:
                delete_confirm_button = driver.find_element(By.CLASS_NAME, "cassette_btn_round--action.js-cassette_delete-confyes")
                ActionChains(driver).move_to_element(delete_confirm_button).click().perform()  # 削除確認ボタンクリック
                time.sleep(1)
            except Exception as e:
                print("削除確定ボタンが見つかりません:", e)
                break

    print("すべてのお気に入りを削除しました。")

finally:
    # ブラウザを閉じる
    driver.quit()