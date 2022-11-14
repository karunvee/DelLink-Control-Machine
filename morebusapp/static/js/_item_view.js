        let dia_ip = 'http://10.195.220.7:9000';
        var dID = document.getElementById("deviceID").value;
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
            output = ""
            output += `<tr>
                            <th>Name</th>
                            <th>Data type</th>
                            <th>Tag ID</th>
                            <th>Register</th>
                            <th>Value</th>
                            <th class="th-indicator">Indicator</th>
                        </tr>`;
            for(let val of data){
                output += `<tr>
                            <td>${val.name}</td>
                            <td>${val.dataType}</td>
                            <td>${val.tid}</td>
                            <td>${val.register}</td>
                            <td><input id="val${val.tid}" class="tag-value" disabled/></td>
                            <td class="td-indicator">
                                <button class="btn-assigned">Unassigned</button>
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

        fetch(dia_ip + '/api/v1/devices')
        .then(response => response.json())
        .then(data => showData(data));

        let api_tag = dia_ip + '/api/v1/devices/'+ String(dID) + '/tags';
        fetch(api_tag)
            .then(response => response.json())
            .then(data => showTag(data));

        setInterval(() => {
                fetch(api_tag).then(response => response.json()).then(data => updateTag(data));
                fetch(dia_ip + '/api/v1/devices').then(response => response.json()).then(data => updateInfo(data));
            }, 2000);
        

        function WriteData(tag_id){
            var tag_value = document.getElementById("TagValue"+tag_id).value;
            let url_api = dia_ip + '/api/v1/devices/'+ String(dID) +'/tags/'+ String(tag_id) +'/value/' + tag_value;
            const initDetails = {
            method: 'PUT',
            headers: {
                'Content-Length': 0,
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyb290IiwianRpIjoiMTBhZWEzNGI3MjRjNGYwMDkzMTE0MjQzZGVmODhmM2YiLCJpYXQiOjE2NjgwNDU4MTksIm5iZiI6MTY2ODA0NTgxOCwiZXhwIjoxNjY4MDg5MDE4LCJpc3MiOiJBUEkuRElBTGluay5ERUxUQSIsImF1ZCI6IkRJQUxpbmsgQVBJIFVzZXIifQ.V1N5C630wk45SlVKq-RHZYB7TPQVxIvpDwIR6URnLv4'
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
        let url_dia = dia_ip + '/devices/97eedc8a4f0a47aeaf2640a03599838f/'+ dID +'/tags'
        var addTag = document.getElementById('addTag');
        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
            if (event.target == addTag) {
                window.open(url_dia, '_blank');
        }
        }