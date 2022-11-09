
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
                                <button>Unassigned</button>
                                <div class="pnl-write-data">
                                <button class="btn-tag-write" id='WriteData' onclick="WriteData(${val.tid})">Write Data</button>
                                <input class="tag-add-value" id="TagValue${val.tid}"/>
                                </div>
                            </td>
                    </tr>`;
            }
            document.querySelector('#machineView').innerHTML += output;
        }
        function updateData(data){
            for(let val of data){
                str = "val" + String(val.tid);
                document.getElementById(str).value = val.value;
            }
        }


        fetch('http://127.0.0.1:5000/api/v1/devices')
        .then(response => response.json())
        .then(data => showData(data));

        let api_tag = 'http://127.0.0.1:5000/api/v1/devices/'+ String(dID) + '/tags';
        fetch(api_tag)
            .then(response => response.json())
            .then(data => showTag(data));
        setInterval(() => {
                fetch(api_tag)
                .then(response => response.json())
                .then(data => updateData(data));
            }, 2000);
        

        function WriteData(tag_id){
            var tag_value = document.getElementById("TagValue"+tag_id).value;
            let url_api = 'http://127.0.0.1:5000/api/v1/devices/'+ String(dID) +'/tags/'+ String(tag_id) +'/value/' + tag_value;
            const initDetails = {
            method: 'PUT',
            headers: {
                'Content-Length': 0,
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyb290IiwianRpIjoiMTEwZTdiYmQwZjc4NDgwY2IyNzgxOGQ0NTRkMTU4MTYiLCJpYXQiOjE2Njc5NjY1MjYsIm5iZiI6MTY2Nzk2NjUyNiwiZXhwIjoxNjY4MDA5NzI2LCJpc3MiOiJBUEkuRElBTGluay5ERUxUQSIsImF1ZCI6IkRJQUxpbmsgQVBJIFVzZXIifQ.1fEilarCWfCTLecpR8IlDytsixQZf7M_HW8745ldf3c'
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
        let url_dia = 'http://192.168.1.254:9000/devices/0a1d921385b4488f840fc5c44d793c9a/'+ dID +'/tags'
        var addTag = document.getElementById('addTag');
        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
            if (event.target == addTag) {
                window.open(url_dia, '_blank');
        }
        }