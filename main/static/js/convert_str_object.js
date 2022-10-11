function mongo_to_obj(str_data){
    let raw_user_data = "{{user_data | safe }}";
    raw_user_data = raw_user_data.replaceAll("\'",'\"');
    raw_user_data = raw_user_data.replace("ObjectId(", '');
    raw_user_data = raw_user_data.replace(")", '');
    const userData = JSON.parse(raw_user_data);
    console.log(userData);
}