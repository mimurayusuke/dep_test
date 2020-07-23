// for input.html
if (document.getElementById("input_success_message") != null) {
    document.getElementById("record latest_title").innerHTML = '今回の記録'
    document.getElementById("record latest_record").style.backgroundColor = 'red'
}

var volume_var = document.getElementById('volume_var');
var weight_record_area = document.getElementById('weight_record_area');
var rep_area = document.getElementById('rep_area');

weight_record_area.addEventListener('change', volume_calc, false);
rep_area.addEventListener('change', volume_calc, false);

function volume_calc() {
    console.log(weight_record_area.value);
    console.log(rep_area.value);
    var wra = weight_record_area.value;
    var re = rep_area.value;
    var result = wra * re;
    console.log(result);

    volume_var.innerHTML = result + 'Kg'
}

// for edit.html
/* {{ id }}の部分はhtmlに記載しないとdjangoのレンダリングが機能しないので、jsファイルからは除外する。
function change_action(){
    var result = confirm('本当に削除しますか？');
    //alertに対してnoの場合の分岐を追加すること。
    if (result) {
        document.getElementById('edit_form').action="/delete/{{ id }}"
    }

}
*/