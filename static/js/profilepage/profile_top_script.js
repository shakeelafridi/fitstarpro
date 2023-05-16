
function DropDownToggle(drop_down_id){
    var get_drop_down = document.getElementById(drop_down_id)
    get_drop_down.classList.toggle('active')
}
function UpdateDropDown_item(btn_id,label_id , drop_down_id){
    var bodyTypeDropDown_btn = document.getElementById(btn_id)
    var GettingLabel = document.getElementById(label_id)
    bodyTypeDropDown_btn.innerHTML = GettingLabel.innerText + '<i class="material-icons arrow_btn">arrow_drop_down</i>'
    DropDownToggle(drop_down_id)
}
function CalculateAge(){
    var user_age_input_ = document.getElementById('ageInput')
    var current_date = new Date()
    var current_year = (current_date.getFullYear())
    var final_value = current_year - user_age_input_.value.split('-')[0]
    return final_value
}
function updateName(){
    var name_input_ = document.getElementById('InputName')
    var ProfileName = document.getElementById('ProfileName')
    ProfileName.innerText = name_input_.value
}
function updateAge(){
    var age_input_ = document.getElementById('ageInput')
    var ageData = document.getElementById('ageData')
    ageData.innerText =  CalculateAge()
}
function updateTrainingRate(){
    var trainingRate_ = document.getElementById('trainingRate')
    var TrainingRateInput = document.getElementById('TrainingRateInput')
    trainingRate_.innerText = TrainingRateInput.value
}
function updateExperience(){
    var Experience_ = document.getElementById('Experience')
    var experience_input = document.getElementById('experience_input')

    Experience_.innerText =  experience_input.value 
};
function updateWeight(){
    var Weight_ = document.getElementById('WeightText')
    var weightInput_ = document.getElementById('WeightInput')
    Weight_.innerText = weightInput_.value
}
function updateHeight(){
    var Height_ = document.getElementById('heightText')
    var height_input_ = document.getElementById('HeightInput')
    var height_in_ft = height_input_.value/12
    var final_height_in_ft = height_in_ft|0
    var height_in_inch = (height_input_.value)%12
    Height_.innerText = final_height_in_ft + 'ft ,' + height_in_inch + 'in'
}
function updateBodyType(){
    var bodyType_ = document.getElementById('Bodytype')
    var final_value = "None"
    let bodytypes_ = document.getElementsByName('bodytype');
        bodytypes_.forEach((bt)=> {
            if (bt.checked) {
                final_value = bt.value
            }
        })
    bodyType_.innerText = final_value
}
function updateLanguages(){
    var languages_text_ = document.getElementById('UserLanguages')
    languages = [
        'English',
        'Urdu',
        'Farsi'
    ]
    var final_output = ""
    for (var i=0; i< languages.length ; i ++) {
        var new_var = languages[i]
        if(document.getElementById(languages[i]).checked){
            final_output += document.getElementById(languages[i]).value
            if (i!=languages.length-1){
                final_output += ","
            }
        }
    }
    languages_text_.innerText = final_output
}
function Show_Hide_content() {
    console.log('Print')
}
function EditSideDetails() {
    var profile_detail_card = document.getElementById('EditDetails').classList.toggle('edit')

}
function UpdateChanges() {
    updateName()
    updateTrainingRate()
    updateAge()
    updateExperience()
    updateWeight()
    updateHeight()
    updateBodyType()
    updateLanguages()
    var profile_detail_card = document.getElementById('EditDetails').classList.toggle('edit')
}