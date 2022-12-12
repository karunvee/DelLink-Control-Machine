       
        var dia_ip = document.getElementById("DIA_http").value;
        var dID = document.getElementById("deviceID").value;
        var guid = document.getElementById("guid").value;
        var lineID = document.getElementById("lineID").value;

       function loginGetToken(data){
            token_ = data.access_token ;
            console.log("token :" + token_);
       }

        let output = "";
        function showData(data){
            for(let val of data){
                if(val.deviceId == dID){
                    let status = "";
                    if(val.status == '1'){
                        status = 'Online';
                    }
                    else{
                        status = 'Offline';
                    }
                    document.getElementById('machineRname').innerHTML = val.name;
                    document.getElementById('machineID').innerHTML = val.deviceId;
                    document.getElementById('machineName').innerHTML  = val.comment;
                    document.getElementById('machineIP').innerHTML  = val.ip;
                    document.getElementById('type').innerHTML  = val.type;
                    document.getElementById('model').innerHTML  = val.model;
                    document.querySelector('#status').innerHTML = `<div class="display ${status}"><label> ${status} </label></div>`;
                }
            }
        }
        function showTag(data){
            document.querySelector('#machineView').innerHTML = ""
            index = 0;
            output = "";
            output += `<tr>
                             <th>No.</th>
                            <th>Name</th>
                            <th>Data type</th>
                            <th>Tag ID</th>
                            <th>Register</th>
                            <th>Value</th>
                            <th class="th-indicator">Indicator</th>
                        </tr>`;
            for(let val of data){
                index += 1;
                output += `<tr>
                            <td>${index}</td>
                            <td>${val.name}<input id="name${val.tid}" value="${val.name}" hidden/></td>
                            <td>${val.dataType}</td>
                            <td>${val.tid}</td>
                            <td>${val.register}<input id="reg${val.tid}" value="${val.register}" hidden/></td>
                            <td><input id="val${val.tid}" class="tag-value" disabled/></td>
                            <td class="td-indicator">
                                <button id="btn-assigned${val.tid}" class="btn-assigned" onclick="openForm(${val.tid})">Unassigned</button>
                                <button id="btn-p-assigned${val.tid}" class="btn-p-assigned" onclick="openForm(${val.tid})" style="display: none; background-color: #ccc; cursor: default;" disabled>Assigned</button>
                                <button id="btn-deleted${val.tid}" class="btn-deleted" onclick="deleteForm(${val.tid})" style="display: none; background-color: rgb(211, 51, 51); margin-left: 5px;"><i class='bx bx-trash' ></i></button>
                                <div class="pnl-write-data">
                                <button class="btn-tag-write" id='WriteData' onclick="WriteData(${val.tid})">Write Data</button>
                                <input class="tag-add-value" id="TagValue${val.tid}"/>
                                </div>
                            </td>
                    </tr>`;
                    
            }
            document.querySelector('#machineView').innerHTML += output;
        }
        function updateTag(data){
            for(let val of data){
                str = "val" + String(val.tid);
                document.getElementById(str).value = val.value; 

                var btn_tag = document.getElementById("bTagValue" + String(val.tid));
                if(btn_tag != null){
                    document.getElementById("bTagValue"+String(val.tid)).value = val.value;
                    const btn = document.querySelector('#btn-TagValue'+String(val.tid));
                    if(val.value == 1){
                        btn.classList.remove("OFF");
                        btn.classList.add("ON");
                    }
                    else{
                        btn.classList.remove("ON");
                        btn.classList.add("OFF");
                    }
                }
                
                var text_tag = document.getElementById("mTagValue" + String(val.tid));
                if(text_tag != null){
                    if(text_tag !== document.activeElement){
                        document.getElementById("mTagValue"+String(val.tid)).value = val.value;
                    }
                }

                var indicator_tag = document.getElementById("indicator"+ String(val.tid))
                if (indicator_tag != null){
                    const ind_show = document.querySelector('#indicator'+String(val.tid));
                    if(val.value == 1){
                        ind_show.classList.remove("OFF");
                        ind_show.classList.add("ON");
                    }
                    else{
                        ind_show.classList.remove("ON");
                        ind_show.classList.add("OFF");
                    }
                }

                var indicator_status = document.getElementById("indicator-status" + String(val.tid));
                if(indicator_status != null ){
                        document.getElementById("indicator-status"+String(val.tid)).value = val.value;
                        StatusMachine(val.value);
                }
                var errorCode = document.getElementById("errorCode" + String(val.tid));
                if(errorCode != null){
                        document.getElementById("errorCode"+String(val.tid)).value = val.value;
                        if(val.value != 0){
                            document.getElementById('alert-message').style.display = "block";
                            var errorMsg = document.getElementById("errorMsg" + String(val.value));
                            if(errorMsg != null){
                                var eMsg = document.getElementById("errorMsg" + String(val.value)).value;
                                document.querySelector('#alert-container').innerHTML = `
                                            <div class="alert">
                                                <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span> 
                                                <strong>Error!</strong> ${eMsg}.
                                            </div>`;
                            }
                            else{
                                document.querySelector('#alert-container').innerHTML = `
                                            <div class="alert">
                                                <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span> 
                                                <strong>Error!</strong> Unknown error message.
                                            </div>`;
                            }
                            
                        }
                        else{
                            document.getElementById('alert-message').style.display = "none";
                            document.querySelector('#alert-container').innerHTML = "";
                        }
                }
 
                // AssignTag status update here
                var ass_tag = document.getElementById("assTag" + String(val.tid));
                if (ass_tag != null)
                {
                    document.getElementById("btn-assigned" + String(val.tid)).style.display = "none";
                    document.getElementById("btn-p-assigned" + String(val.tid)).style.display = "block";
                    document.getElementById("btn-deleted" + String(val.tid)).style.display = "block";
                }
            }  
        }
        function updateInfo(data){
            for(let val of data){
                if(val.deviceId == dID){
                    let status = "";
                    if(val.status == '1'){
                        status = 'Online';
                    }
                    else{
                        status = 'Offline';
                    }
                    document.querySelector('#status').innerHTML = `<div class="display ${status}"><label> ${status} </label></div>`;
                }
            }
        }
        var details = {
            'username': 'root',
            'password': 'admin',
        };
        var formBody  = [];
        for (var property in details) {
          var encodedKey = encodeURIComponent(property);
          var encodedValue = encodeURIComponent(details[property]);
          formBody.push(encodedKey + "=" + encodedValue);
        }
        formBody = formBody.join("&");

        fetch(String(dia_ip) + '/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Content-Length': 0,
        },
        body: formBody,
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
            loginGetToken(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });

        fetch(String(dia_ip) + '/api/v1/devices')
        .then(response => response.json())
        .then(data => showData(data));

        let api_tag = String(dia_ip) + '/api/v1/devices/'+ String(dID) + '/tags';
        fetch(api_tag)
            .then(response => response.json())
            .then(data => showTag(data));

        setInterval(() => {
                fetch(String(dia_ip) + '/api/v1/devices').then(response => response.json()).then(data => updateInfo(data));
            }, 2000);
        setInterval(() => {
                fetch(api_tag).then(response => response.json()).then(data => updateTag(data));
            }, 500);
        

        function WriteData(tag_id, tg = 0){
            $("body").css("cursor", "progress");
            console.log("token :" + token_);
            if (token_ == ""){
                alert("Authorization error : Token is empty!!");
            }
            else{
                switch(tg){
                    case 1:
                        var tag_value = document.getElementById("mTagValue"+tag_id).value;
                        break;
                    case 2:
                        var tag_value = document.getElementById("bTagValue"+tag_id).value;
                        tag_value = 1 - tag_value ;
                        break;
                    default:
                        var tag_value = document.getElementById("TagValue"+tag_id).value;
                }
                let url_api = String(dia_ip) + '/api/v1/devices/'+ String(dID) +'/tags/'+ String(tag_id) +'/value/' + tag_value;
                const initDetails = {
                method: 'PUT',
                headers: {
                    'Content-Length': 0,
                    'Authorization': "Bearer " + token_
                },
                }
                fetch(url_api,initDetails).then( response =>
                    {
                        if ( response.status == 401 )
                        {
                            console.log('Status Code: 401 Unauthorized');
                            alert('Status Code: 401 Unauthorized');
                            return;
                        }
                        else if(response.status != 204){
                            let msg = 'Value :' + tag_value + ', MachineID :'+ dID +', Tag ID :' + tag_id + ', Status Code: ' +
                                response.status;
    
                            console.log(msg);
                            alert(msg);
                            return;
                        }
                        // alert('Write the value success!');
                        console.log( response.headers.get( "Content-Type" ) );
                        return 0;
                    }
                    )
            }
            $("body").css("cursor", "default");
        }
        function openForm(tid) {
            // document.getElementById('tagName').innerText = document.getElementById("name" + tid).value;
            document.getElementById('tagName').value = document.getElementById("name" + tid).value;

            // document.getElementById('register').innerText = document.getElementById("reg" + tid).value;
            document.getElementById('register').value = document.getElementById("reg" + tid).value;

            document.getElementById('tagID').innerText = tid;
            document.getElementById('tagID').value = tid;

            // Appearance Assignment Form
            document.getElementById('assignForm').style.display = "block";

            // clear
            document.getElementById("data_type").value = "";
            document.getElementById('datatype_bit').style.display = "none";
            document.getElementById('datatype_text').style.display = "none";
            document.getElementById('btn-add').style.display = "none";
        }

        function deleteForm(tid){
            // Appearance Comfirm Form
            document.getElementById('confirmForm').style.display = "block";
            document.querySelector('#confirmForm').innerHTML = 
            `<div class="confirmForm-container">
            <div class="confirmForm-content">
                <h1>Question ?</h1>
                <p>Are you sure you want to delete this indicator id :${tid}, line :${lineID}, DeviceID :${dID}?</p>
                <div class="clearfix">
                    <button class="btn-delete yes" onclick="location.href='/delete_indicator/ln${lineID}id${dID}tag_id${tid}/';">Yes, I'm sure</button>
                    <button class="btn-delete no" type="button" onclick="document.getElementById('confirmForm').style.display='none'">No</button>
                </div>
            </div>
            </div>`;
        }
        const getDataType = () =>{
            let inputValue = document.getElementById("data_type").value; 
            if(inputValue == "BIT"){
                document.getElementById('datatype_bit').style.display = "block";
                document.getElementById('datatype_text').style.display = "none";
                document.getElementById('btn-add').style.display = "block";
            }
            else if(inputValue == ""){
                alert("Please select the data type");
                document.getElementById('datatype_bit').style.display = "none";
                document.getElementById('datatype_text').style.display = "none";
                document.getElementById('btn-add').style.display = "none";
            }
            else{
                document.getElementById('datatype_bit').style.display = "none";
                document.getElementById('datatype_text').style.display = "block";
                document.getElementById('btn-add').style.display = "block";
            }
            }

        let url_dia = String(dia_ip) + '/devices/' + guid + '/'+ dID +'/tags'

        function openDIAform(){
            window.open(url_dia,"", "width=1200,height=750");
        }
        
        p_val = "";
        function StatusMachine(val){
            const sg = document.querySelector('#status-green');
            const sy = document.querySelector('#status-yellow');
            const sr = document.querySelector('#status-red');
            if( val != p_val){
                switch (val){
                    case "0":
                        document.getElementById("text-indicator-status").innerText = "Normal";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sg.classList.add("green");
                        break;
                    case "1":
                        document.getElementById("text-indicator-status").innerText = "Error";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sr.classList.add("red");
                        break;
                    case "2":
                        document.getElementById("text-indicator-status").innerText = "Pause";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    case "3":
                        document.getElementById("text-indicator-status").innerText = "standby";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    case "4":
                        document.getElementById("text-indicator-status").innerText = "Wait for material";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    case "5":
                        document.getElementById("text-indicator-status").innerText = "Output full material";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    case "6":
                        document.getElementById("text-indicator-status").innerText = "Material low";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    case "7":
                        document.getElementById("text-indicator-status").innerText = "Change line";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        sy.classList.add("yellow");
                        break;
                    default:
                        document.getElementById("text-indicator-status").innerText = "Unknown";
                        sg.classList.remove("green");
                        sy.classList.remove("yellow");
                        sr.classList.remove("red");
                        break;
                }
            }
            p_val = val;
            
        }
