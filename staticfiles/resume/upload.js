
class FileStreamer {
    constructor(file) {
        this.file = file;
        this.offset = 0;
        this.defaultChunkSize = 6000000; // bytes
        this.rewind();
    }
    rewind() {
        this.offset = 0;
    }
    isEndOfFile() {
        return this.offset >= this.getFileSize();
    }

    readBlockAsText(m,n) {
        length = m
        const fileReader = new FileReader();
        const blob = this.file.slice(m,n);
        return new Promise((resolve, reject) => {
            fileReader.onload = (event) => {
                const target = (event.target);
                if (target.error == null) {
                    const result = target.result;
                    // if (result.length > 6000000 && ((this.offset)/length) > (this.file.length/length))
                    // {
                    console.log('PartNo:',part_no);
                    console.log('file sliced',this.offset,'to', this.offset + length)
                    console.log('Reolved file length',result.length);
                    console.log('File length',this.file.size);
                    // }
                    // this.offset += result.length;
                    console.log('File length',(result.length/(1024*1024)),'mb');
                    this.testEndOfFile();
                    resolve(result);
                    // resolve('small');
                }
                else {
                    reject(target.error);
                }
            };
            fileReader.readAsArrayBuffer(blob);
        });
    }
    testEndOfFile() {
        if (this.isEndOfFile()) {
            console.log('Done reading file');
        }
    }
    getFileSize() {
        return this.file.size;
    }
}



$('#upload_button').click(async function(){
    console.log("Pressed");
    var file = $('#upload')[0].files[0];
    var chunkSize = 1024*1024*5;
    var fileSize = (file.size - 1);
    var uploadID = '';

        //get the upload ID for the file selected
        try { 
    let res = await timeoutPromise(10*60*1000, fetch("/initiate_upload", {
            method: 'POST',
            body:  JSON.stringify({'file_name':file.name }),
            headers:{
                        'X-CSRFToken':  $.cookie('csrftoken'),
                        'Content-Type': 'application/json'
                   }
          }));
  uploadID = res.upload_id;
  } catch(error) {
    // might be a timeout error
    console.log('Error for file uploadID');
  }

  part_no = 1;
  var data ;
  total_part = file.size/6000000;
  etag_list = {
      'Parts':[

      ]
  };
    const fileStreamer = new FileStreamer(file);

    // new code
    var files = document.getElementById('upload').files;

    var file = files[0];

    var size = file.size;
    var chunksize = 6000000;
    var x = 0;
    while (x < size) {
        //
        try { 
        let res = await timeoutPromise(10*60*1000, fetch("/url_multi", {
                method: 'POST',
                body:  JSON.stringify({
                    'key':file.name,
                    'part_no':part_no,
                    'upload_id':uploadID
                    }),
                headers:{
                            'X-CSRFToken':  $.cookie('csrftoken'),
                            'Content-Type': 'application/json'
                    }
            }));
            upload_url = res.url;
    console.log(res);
    } catch(error) {
        // might be a timeout error
        console.log('error');
    }
    //get data chunk from the file reader
    console.log('Total part',total_part);
    var data;
    if((x+chunksize)<size){
            console.log(x, x+chunksize);
             data = await fileStreamer.readBlockAsText(x, x+chunksize);
        }
        else{
            console.log(x,size,'end');
             data = await fileStreamer.readBlockAsText(x,size);
        }
        x+=chunksize;// to prepare for next loop

    console.log('Data size',data.length);
    console.log('Ad bytes',data.length < (5*1024*1024), part_no > total_part)
    console.log('Part_no < total', part_no,total_part);
   
    try {
        console.log(upload_url); 
        let res = await timeoutPromise(10*60*1000, fetch(upload_url, {
                method: 'PUT',
                body:data,
                headers:{
                    'Accept': 'application/octet-stream'
                    }
            }));
            console.log(res);
            etag_list.Parts.push({
                "ETag":res,
                "PartNumber":part_no
             } );
        // console.log(res.headers);
        }
        catch(error){
            console.log(error);
        }
    // console.log(res.headers);
    //   console.log(data);
    part_no = part_no + 1;
    
}

try { 
    let res = await timeoutPromise(10*60*1000, fetch("/complete_upload", {
            method: 'POST',
            body:  JSON.stringify({
                'file_name':file.name,
                'upload_id':uploadID,
                'multi_part_etags':etag_list
                }),
            headers:{
                        'X-CSRFToken':  $.cookie('csrftoken'),
                        'Content-Type': 'application/json'
                   }
          }));
  console.log(res);
  } catch(error) {
    // might be a timeout error
    console.log('Error for file uploadID');
  }
console.log(etag_list);
});




//fetch Prommise function
function timeoutPromise(ms, promise) {
  return new Promise((resolve, reject) => {
    const timeoutId = setTimeout(() => {
      reject(new Error("promise timeout"))
    }, ms);
    promise.then(
      (res) => {
        clearTimeout(timeoutId);
        var etag = res.headers.get('etag');
//         for(let entry of res.headers.entries()) {
//     console.log(entry);
//   }
       if (etag != null)
        {
        resolve(etag);
        }
        else{
            resolve(res.json());
        }
      },
      (err) => {
          console.log('Line 147',err);
        clearTimeout(timeoutId);
        reject(err);
      }
    );
  })
}