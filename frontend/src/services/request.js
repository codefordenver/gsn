const API_ROOT = 'http://127.0.0.1:8000/';

export function request({
  url,
  method='GET',
  headers={'Content-Type': 'application/json'},
  body
}) {
  if (url) {
    return fetch(`${API_ROOT}${url}`,{method, headers, body});
  }
}
