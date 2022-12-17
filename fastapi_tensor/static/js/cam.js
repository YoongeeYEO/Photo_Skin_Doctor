function cam() {
    $.ajax({
        url: "/cam",
        type: "post",
        contentType: false,
        processData: false,
        success: function(res){
            updatetags_upload(res)
            // console.log(res)
        }

    })
}

function updatetags_upload(data) {
    console.log(data)
    let original = `<img src="/${data.thumb_path}" class="responsive" alt="" id="origin_img">`;
    let pred = `<h3 id="pred"><br /><br />${data.Predicted_name}</h3>`;
    $("#original").html(original);
    $("#pred").html(pred);

    $("#howto").html("Drag and Drop file here<br />Or<br />Click to Upload")
}