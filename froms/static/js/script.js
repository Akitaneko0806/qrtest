// フォーム送信のAjax処理を削除し、通常のフォーム送信を使用
$(document).ready(function() {
    // 既存のJavaScript処理（必要に応じて）

    // 例: フォームのバリデーション
    $('#survey-form').on('submit', function(e) {
        // フォームのバリデーションロジックをここに記述
        // エラーがある場合は e.preventDefault() を呼び出してフォーム送信を止める
    });
});