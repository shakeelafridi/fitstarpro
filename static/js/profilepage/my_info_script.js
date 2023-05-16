function Show_Edit_Details(show_able_content_id , edit_able_content_id) {
    document.getElementById(show_able_content_id).classList.toggle('active')
    document.getElementById(edit_able_content_id).classList.toggle('edit')
}
function toggle_edit_info(show_able_content , hide_able_content){
     let data1 = document.getElementsByClassName(show_able_content);
     let data2 = document.getElementsByClassName(hide_able_content);
     for (let i = 0; i < data1.length; i++) {
         data1[i].style.display = "initial";
     }
     for (let i = 0; i < data2.length; i++) {
         data2[i].style.display = "none";
     }
}
function HideAllTabsSectionsButtons(){
    var all_tabs_body = document.getElementsByClassName('profile_detail_content')
    var all_tabs_buttons = document.getElementsByClassName('tabButton')
    for(var i=0; i<all_tabs_buttons.length;i++ ){
        all_tabs_buttons[i].classList.remove("active")
    }
    for(var i=0; i<all_tabs_body.length;i++ ){
        all_tabs_body[i].classList.remove("active")
    }
}
function ShowParticularTab(Tab_btn_ID ,Tab_body_ID ){
    document.getElementById(Tab_btn_ID).classList.toggle('active')
    document.getElementById(Tab_body_ID).classList.toggle('active')
}

function UpdateNavTab(Tab_btn_ID , Tab_body_ID){
    HideAllTabsSectionsButtons()
    ShowParticularTab(Tab_btn_ID ,Tab_body_ID )
}
function addNewAwards() {
    $('.fitnessAwardMain').append('<div class="row fitnessAwardMainItem" style="margin-bottom: 10px">\n' +
        '                            <div class="col-10 p-0">\n' +
        '                                <input class="form-control mt-0 fitness_awards_multiple_field">\n' +
        '                            </div>\n' +
        '                            <div class="col-2 p-0 text-right">\n' +
        '                                <a style="background-color: red; padding: 6px; border-radius: 25px; color: white; float: right;" onclick="removeNewAwards()">\n' +
        '                                    <i class="material-icons">delete</i>\n' +
        '                                </a>\n' +
        '                            </div>\n' +
        '                        </div>')
}

function removeNewAwards(){
    console.log(event.target.closest('.fitnessAwardMainItem'))
    event.target.closest('.fitnessAwardMainItem').remove();
}

$( "#info_tab_submit_fitness_professional" ).submit(function( event ) {
    var fitnessAwards = $('.fitness_awards_multiple_field').map(function(){
             return "'" + this.value + "'";
          }).get();
    console.log('fitness awards', fitnessAwards);
    $('#fitnessAwards').val(fitnessAwards.toString());


    // for product Review
    var productNameReview = $('.product_review_name_multiple_field').map(function(){
        return "'" + this.value + "'";
    }).get();

    var productReview = $('.product_review_multiple_field').map(function(){
        return "'" + this.value + "'";
    }).get();

    var productReviewStar = $('.productReviewRatingValue').map(function(){
        return "'" + this.value + "'";
    }).get();

    $('#productNameReviewValue').val(productNameReview.toString());
    $('#productReviewValue').val(productReview.toString());
    $('#productReviewStarValue').val(productReviewStar.toString());

   // for sponcer Images
   var sponsorImagesName = $('.sponsorImagesName').map(function(){
       return this.value;
   }).get();

   console.log(sponsorImagesName,'----------------names');

   $('#sponsorImagesValueMain').empty();
   var sponsorImagesValue = $('.sponsorImagesValue').map(function(){
       return this.value;
   }).get();
   console.log('sponsorImagesValue', sponsorImagesValue);
   $('#sponsorImagesNameValue').val(sponsorImagesName.toString());
   $('#sponsorImagesValueValue').val(sponsorImagesValue.toString());

   for ( let i = 0; i <  sponsorImagesValue.length; i++)  {
       console.log(sponsorImagesValue[i],'----------------loop images');
       $('.sponsorImagesNameMain').append('<input type="file" hidden name="sponsorImagesNameValues" value="'+sponsorImagesValue[i]+'">')
   }

   for ( let i = 0; i <  sponsorImagesName.length; i++)  {
       console.log(sponsorImagesName[i],'---------------loop names');
    $('.sponsorImagesMain').append('<input type="text" hidden name="sponsorImagesss" value="'+sponsorImagesName[i]+'">')
}


//    return false;
     return true;

});


function addNewProductReview() {
    let data = document.getElementsByClassName('product_review_name_multiple_field');
    let len = data.length + 1;
    $('.productReviewsMain').append('<div class="row productReviewsMainItem" id style="margin-bottom: 10px">\n' +
        '                            <div class="col-10 p-0 row">\n' +
        '                                <input class="col-3 form-control mt-0 product_review_name_multiple_field"\n' +
        '                                       style="margin-right: 2px" placeholder="Product" >\n' +
        '                                <input class="col-4 form-control mt-0 product_review_multiple_field"\n' +
        '                                       style="margin-right: 5px" placeholder="Review" >\n' +
        '                                <div class="col-3">\n' +
        '                                    <div class="rating" style="width:90px;">\n' +
        '                                    <input id="star5'+len+'" name="star'+len+'" type="radio" value="5" class="radio-btn hide" onchange="updateRatingValue('+len+', 5)"/>\n' +
        '                                    <label for="star5'+len+'" >☆</label>\n' +
        '                                    <input id="star4'+len+'" name="star'+len+'" type="radio" value="4" class="radio-btn hide" onchange="updateRatingValue('+len+', 4)"/>\n' +
        '                                    <label for="star4'+len+'" >☆</label>\n' +
        '                                    <input id="star3'+len+'" name="star'+len+'" type="radio" value="3" class="radio-btn hide" onchange="updateRatingValue('+len+', 3)"/>\n' +
        '                                    <label for="star3'+len+'" >☆</label>\n' +
        '                                    <input id="star2'+len+'" name="star'+len+'" type="radio" value="2" class="radio-btn hide" onchange="updateRatingValue('+len+', 2)"/>\n' +
        '                                    <label for="star2'+len+'" >☆</label>\n' +
        '                                    <input id="star1'+len+'" name="star'+len+'" type="radio" value="1" class="radio-btn hide" onchange="updateRatingValue('+len+', 1)"/>\n' +
        '                                    <label for="star1'+len+'" >☆</label>\n' +
        '                                    <div class="clear"></div>\n' +
        '                                </div>\n' +
        '                                </div>\n' +
        '                                <div class="col-1">\n' +
        '                                  <input class="productReviewRatingValue productReviewRatingValue'+len+'" type="number" style="width: 30px;visibility: hidden">\n' +
        '                                </div>\n' +
        '                            </div>\n' +
        '\n' +
        '                            <div class="col-2 p-0 text-right">\n' +
        '                                <a style="background-color: red; padding: 6px; border-radius: 25px; color: white; float: right;"\n' +
        '                                onclick="removeProductReview()">\n' +
        '                                    <i class="material-icons">delete</i>\n' +
        '                                </a>\n' +
        '                            </div>\n' +
        '                        </div>')
}

function removeProductReview(){
    console.log(event.target.closest('.productReviewsMainItem'))
    event.target.closest('.productReviewsMainItem').remove();
}

function updateRatingValue(classNameId, value){
    $('.productReviewRatingValue'+classNameId).val(Number(value));
}

var imgCounter = 0;
function addNewSponsorImages() {
    imgCounter+=1;
    $('.sponsorImagesMain').append('<div class="row sponsorImagesMainItem" id style="margin-bottom: 10px">\n' +
        '                            <div class="col-10 p-0 row">\n' +
        '                                <input class="col-5 form-control mt-0 sponsorImagesName"\n' +
        '                                       style="margin-right: 2px" name="sponsorImagesName" placeholder="Name" required>\n' +
        '                                <input class="col-6 form-control mt-0 sponsorImagesValue"\n' +
        '                                       style="margin-right: 5px" required name="sponserImg'+imgCounter+'" type="file">\n' +
        '                            </div>\n' +
        '\n' +
        '                            <div class="col-2 p-0 text-right">\n' +
        '                                <a style="background-color: red; padding: 6px; border-radius: 25px; color: white; float: right;"\n' +
        '                                   onclick="removeNewSponsorImages()">\n' +
        '                                    <i class="material-icons">delete</i>\n' +
        '                                </a>\n' +
        '                            </div>\n' +
        '                        </div>');

        $("#countImages").val(imgCounter);

}



function removeNewSponsorImages() {
    event.target.closest('.sponsorImagesMainItem').remove();
    // imgCounter-=1;
    // $("#countImages").val(imgCounter);
}


$( "#info_tab_submit_fitness_model" ).submit(function( event ) {

    // for product Review
    var productNameReview = $('.product_review_name_multiple_field').map(function(){
        return "'" + this.value + "'";
    }).get();

    var productReview = $('.product_review_multiple_field').map(function(){
        return "'" + this.value + "'";
    }).get();

    var productReviewStar = $('.productReviewRatingValue').map(function(){
        return "'" + this.value + "'";
    }).get();

    $('#productNameReviewValue').val(productNameReview.toString());
    $('#productReviewValue').val(productReview.toString());
    $('#productReviewStarValue').val(productReviewStar.toString());
//
//    // for sponcer Images
//    var sponsorImagesName = $('.sponsorImagesName').map(function(){
//        return this.value;
//    }).get();
//
//    $('#sponsorImagesValueMain').empty();
//    var sponsorImagesValue = $('.sponsorImagesValue').map(function(){
//        return this.value;
//    }).get();
//    console.log('sponsorImagesValue', sponsorImagesValue);
//    $('#sponsorImagesNameValue').val(sponsorImagesName.toString());
//    $('#sponsorImagesValueValue').val(sponsorImagesValue.toString());
//
//    for ( let i = 0; i <  sponsorImagesValue.length; i++)  {
//        $('.sponsorImagesValueMain').append('<input type="file" name="sponsorImagesNameValue" value="'+sponsorImagesValue[i]+'">')
//    }


//    return false;
     return true;

});


$( "#info_tab_submit_fitness_center" ).submit(function( event ) {

    // for product Review
    var productNameReview = $('.product_review_name_multiple_field').map(function(){
        return "'" + this.value + "'";
    }).get();

    var productReview = $('.product_review_multiple_field').map(function(){
        return "'" + this.value + "'";
    }).get();

    var productReviewStar = $('.productReviewRatingValue').map(function(){
        return "'" + this.value + "'";
    }).get();

    $('#productNameReviewValue').val(productNameReview.toString());
    $('#productReviewValue').val(productReview.toString());
    $('#productReviewStarValue').val(productReviewStar.toString());

     return true;

});

