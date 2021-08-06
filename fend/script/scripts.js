var lastAdded = 1

function JSON_to_URLEncoded(element, key, list) {
    var list = list || [];
    if (typeof (element) == 'object') {
        for (var idx in element)
            JSON_to_URLEncoded(element[idx], key ? key + '[' + idx + ']' : idx, list);
    } else {
        list.push(key + '=' + encodeURIComponent(element));
    }
    return list.join('&');
}

function submitVerify() {
    var prms = {
        upload_id: $("#uploadId1").val(),
        skip_verify: $('input[name="skipVerify"]:checked').val(),
        skip_db_search: $('input[name="skipDbSearch"]:checked').val(),
        skip_liveness: $('input[name="skipLiveness"]:checked').val()
    };

    const toUrlEncoded = JSON_to_URLEncoded(prms);

    console.log(toUrlEncoded)
    $.ajax({
        type: 'POST',
        url: "https://reco.filesdna.com/api/verify",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'deflate'
        },
        contentType: 'application/x-www-form-urlencoded; charset=utf-8',
        data: toUrlEncoded,
        processData: false,
        success: function (response) {
            console.log("Got a response from /verify.")
            console.log(response);
            $("#response-div-verify").html(JSON.stringify(response));
        }
    })
    return false
}

function submitUploadToDb() {
    var prms = {
        upload_id: $("#uploadId2").val(),
        delete_pickles: $('input[name="deletePickles"]:checked').val(),
        rebuild_db: $('input[name="rebuildDb"]:checked').val(),
        name: $('#personName').val(),
        in_place: $('input[name="inPlace"]:checked').val(),

    };

    const toUrlEncoded = JSON_to_URLEncoded(prms);

    console.log(toUrlEncoded)
    $.ajax({
        type: 'POST',
        url: "https://reco.filesdna.com/api/upload_db",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'deflate'
        },
        contentType: 'application/x-www-form-urlencoded; charset=utf-8',
        data: toUrlEncoded,
        processData: false,
        success: function (response) {
            console.log("Got a response from /upload_db.")
            console.log(response);
            $("#response-div-db").html(JSON.stringify(response));
        }
    })
    return false
}

function submitImages() {
    var id = $("#id").val();
    var formData = new FormData(document.getElementById("uploadForm"));
    $.ajax({
        url: 'https://reco.filesdna.com/api/upload_imgs?id=' + id,
        type: 'POST',
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
        success: function (response) {
            console.log("Got a response from /upload_imgs.")
            console.log(response);
            $("#response-div").html(JSON.stringify(response));
        }
    });
    return false

}

function appendToForm() {
    lastAdded += 1;
    $("<input type='file' value='File' />")
        .attr("name", `file_${lastAdded}`)
        .attr("value", `img_${lastAdded}`)
        .attr("id", `file_${lastAdded}`)
        .appendTo("#files");

    $("<br />")
        .attr("id", `lr_${lastAdded}`)
        .appendTo("#files");

}

function removeFile() {
    $(`#file_${lastAdded}`).remove()
    $(`#lr_${lastAdded}`).remove()
    if (lastAdded > 2) {
        lastAdded -= 1
    }

}