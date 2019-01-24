const API_ROOT = 'http://127.0.0.1:8000/';

export function request({
  url,
  method='GET',
  headers={'Content-Type': 'application/json'},
  body
}) {
  if (url) {
    return fetch(`${API_ROOT}${url}`,{method, headers, body})
    .then(result => {
      const {status, statusText} = result;
      if (status >= 200 && status < 300) return result.json();
      if (status >= 400 && status < 600) return Promise.reject(new Error(statusText));
    })
    // .catch(error => Promise.reject(error));
  }
}
