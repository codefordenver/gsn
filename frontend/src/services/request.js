const API_ROOT = 'http://127.0.0.1:8000/';

export function request({
  url,
  method='GET',
  headers={'Content-Type': 'application/json'},
  body
}) {
  return new Promise((resolve, reject)=>{
    if (url) {
      fetch(`${API_ROOT}${url}`,{method, headers, body})
      .then(result => {
        const {status, statusText} = result;
        if (status >= 400 && status < 600){
          reject (statusText);
        } else if (status >= 200 && status < 300) {
          resolve (result.json());
        } else {
          reject (`Uncaught status range (code: ${status}, text: ${statusText})`);
        }
      }).catch((error)=>{
        console.error({error});
        reject (error.message || 'Unknown fetch issue');
      });
    } else {
      reject ('No url given to request');
    }
  });

}
