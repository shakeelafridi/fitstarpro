
$('.pop').on('click', function() {
    var bg = $(this).css('background-image');
    bg = bg.replace('url(','').replace(')','').replace(/\"/gi, "");
    $('.imagepreview').attr('src', bg)
});

$('.popsuccesstory').on('click', function() {
    var bg = $(this).attr('src');
    $('.imagepreview').attr('src', bg)
});


$('.profileImageEditIcon').on('click', function() {
    var bg = $('.profileImageBackgroundCard').css('background-image');
    bg = bg.replace('url(','').replace(')','').replace(/\"/gi, "");
    $('.profileImagePreview').attr('src', bg)
});

var profile_image_uploading = document.getElementById('profile_image_uploading')
profile_image_uploading.addEventListener('change' , function(){
    var fileChoosenID_tag = document.getElementById('profile_image_uploading_name')
    fileChoosenID_tag.innerText = this.files[0].name
})

var gallery_image = document.getElementById('gallery_image')
gallery_image.addEventListener('change' , function(){
    console.log('event trigger')
    var fileChoosenID_tag = document.getElementById('gallery_image_file_uploaded_name')
    if (this.files.length == 1){
        text_ = this.files.length + " file is uploaded"
    }
    else {
        text_ = this.files.length + " files are uploaded"
    }

    fileChoosenID_tag.innerText = text_
})


var before_image = document.getElementById('before_image')
before_image.addEventListener('change' , function(){
    var fileChoosenID_tag = document.getElementById('before_image_file_uploaded_name')
    fileChoosenID_tag.innerText = this.files[0].name
})

var after_image = document.getElementById('after_image')
after_image.addEventListener('change' , function(){
    var fileChoosenID_tag = document.getElementById('after_image_file_uploaded_name')
    fileChoosenID_tag.innerText = this.files[0].name
})

function readURL(input, src_div) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $(src_div).attr('src', e.target.result);
            $(src_div).css("display", "block");
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$("#before_image").change(function(){
    readURL(this, '#before_image_preview');
});

$("#after_image").change(function(){
    readURL(this, '#after_image_preview');
});

//$("#profile_image_uploading").change(function(){
//    readURL(this, '.profileImagePreview');
//});

//----------------------------------------------------

let result = document.querySelector('.result'),
img_result = document.querySelector('.img-result'),
cropped = document.querySelector('.cropped'),
save = document.querySelector('.save'),
upload = document.querySelector('#profile_image_uploading'),
cropper = '';

upload.addEventListener('change', (e) => {
  if (e.target.files.length) {
    const reader = new FileReader();
    $('.profileImagePreview').css('display', 'none');
    reader.onload = (e)=> {
      if(e.target.result){
				let img = document.createElement('img');
				img.id = 'image';
				img.src = e.target.result
				result.innerHTML = '';
        result.appendChild(img);
				save.classList.remove('hide');
				cropper = new Cropper(img, {
                    dragMode: 'move',
                    autoCropArea: 1,
                    restore: false,
                    guides: false,
                    center: true,
                    highlight: false,
                    cropBoxMovable: true,
                    cropBoxResizable: false,
                    toggleDragModeOnDblclick: false,
                    data:{
                      width: 400,
                      height:  400,
                    },
                });
      }
    };
    reader.readAsDataURL(e.target.files[0]);
  }
});

save.addEventListener('click',(e)=>{
  e.preventDefault();
  let imgSrc = cropper.getCroppedCanvas({
		width: 400,
		height: 400
	}).toDataURL();
  cropped.src = imgSrc;
  $("#cropped_image").val(imgSrc);
  $("#profile_image_upload").submit();
});

