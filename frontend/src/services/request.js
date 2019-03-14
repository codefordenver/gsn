// const API_ROOT = 'http://127.0.0.1:8000/';

const API_ROOT = 'http://gsndev.com/';

export function request({
  url,
  method = 'GET',
  headers = { 'Content-Type': 'application/json' },
  body,
}) {
  return new Promise((resolve, reject) => {
    if (url) {
      fetch(`${API_ROOT}${url}`, { method, headers, body })
        .then((result) => {
          const { status, statusText } = result;
          if (status >= 400 && status < 600) {
            reject(new Error(`(code: ${status}, text: ${statusText})`));
          } else if (status >= 200 && status < 300) {
            resolve(result.json());
          } else {
            reject(new Error(`Uncaught status range (code: ${status}, text: ${statusText})`));
          }
        }).catch((error) => {
          console.error({ error });
          reject(error);
        });
    } else {
      reject(new Error('No url given to request'));
    }
  });
}
