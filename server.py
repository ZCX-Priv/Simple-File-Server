import os
import socket
import sys
import threading
import urllib.parse

favicon = [0x00,0x00,0x01,0x00,0x01,0x00,0x10,0x10,0x00,0x00,0x01,0x00,0x18,0x00,0x68,0x03,0x00,0x00,0x16,0x00,0x00,0x00,0x28,0x00,0x00,0x00,0x10,0x00,0x00,0x00,0x20,0x00,0x00,0x00,0x01,0x00,0x18,0x00,0x00,0x00,0x00,0x00,0x68,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
icons= {
    ".zip":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M12.167 3h-3.75v2.083h1.25V8H6.333V5.083h1.25V3h-3.75a.417.417 0 0 0-.416.417v9.166c0 .23.186.417.416.417h8.334c.23 0 .416-.186.416-.417V3.417A.416.416 0 0 0 12.167 3Zm-3.334 8.333H7.167V10.5h1.666v.833ZM7.167 9.667h1.666v-.834H7.167v.834Z" fill="#5654BC"/><path fill="#FF9CAC" d="M7.167 5.917h1.667v1.25H7.167z"/></svg>'
    ,".doc":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M2.5 13.5v-11A.5.5 0 0 1 3 2h10a.5.5 0 0 1 .5.5v11a.5.5 0 0 1-.5.5H3a.5.5 0 0 1-.5-.5Zm5-9h-3v3h3v-3Zm4 7h-7v-1h7v1Zm-7-2h7v-1h-7v1Zm7-2h-3v-1h3v1Zm-3-2h3v-1h-3v1Z" fill="#3965BD"/></svg>'
    ,".js":'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="32" height="32" viewBox="0 0 32 32"><path fill="#f5de19" d="M2 2h28v28H2z"></path><path d="M20.809 23.875a2.866 2.866 0 0 0 2.6 1.6c1.09 0 1.787-.545 1.787-1.3c0-.9-.716-1.222-1.916-1.747l-.658-.282c-1.9-.809-3.16-1.822-3.16-3.964c0-1.973 1.5-3.476 3.853-3.476a3.889 3.889 0 0 1 3.742 2.107L25 18.128A1.789 1.789 0 0 0 23.311 17a1.145 1.145 0 0 0-1.259 1.128c0 .789.489 1.109 1.618 1.6l.658.282c2.236.959 3.5 1.936 3.5 4.133c0 2.369-1.861 3.667-4.36 3.667a5.055 5.055 0 0 1-4.795-2.691Zm-9.295.228c.413.733.789 1.353 1.693 1.353c.864 0 1.41-.338 1.41-1.653v-8.947h2.631v8.982c0 2.724-1.6 3.964-3.929 3.964a4.085 4.085 0 0 1-3.947-2.4Z"></path></svg>'
    ,".json":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><g fill-rule="evenodd" clip-rule="evenodd"><path d="M5.5 3.5h-1a1 1 0 0 0-1 1v2a1 1 0 0 1-1 1H2v1h.5a1 1 0 0 1 1 1v2c0 .55.465.865 1 1h1v-1h-1V9a1 1 0 0 0-1-1 1 1 0 0 0 1-1V4.5h1v-1Zm7 1a1 1 0 0 0-1-1h-1v1h1V7a1 1 0 0 0 1 1 1 1 0 0 0-1 1v2.5h-1v1h1a1 1 0 0 0 1-1v-2a1 1 0 0 1 1-1h.5v-1h-.5a1 1 0 0 1-1-1v-2Z" fill="#89DDFF"/><path d="M6 7.5a.5.5 0 1 1 0 1 .5.5 0 0 1 0-1Zm2 0a.5.5 0 1 1 0 1 .5.5 0 0 1 0-1Zm2.5.5a.5.5 0 1 0-1 0 .5.5 0 0 0 1 0Z" fill="#FFCB6B"/></g></svg>'
    ,".java":'<svg width="14" height="14" fill="none" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#a)"><path d="M9.749 3.064c-1.063.32-2.214.76-2.845 1.722-.45.7-.123 1.6.404 2.158.365.359.22.948-.153 1.242-.392.342.06.282.288.117.555-.343 1.176-.97.938-1.684-.186-.54-.887-.987-.64-1.618.481-.867 1.483-1.249 2.237-1.838.29-.193-.117-.073-.23-.1ZM7.895 0l.1.464c.582 2.307-2.317 2.835-3.01 4.471-.284.836.376 1.599.905 2.17.363.368.732.742 1.157 1.048-.194-.981-1.286-1.613-1.188-2.668.195-1.013 1.257-1.457 1.866-2.188C8.736 2.174 8.96.999 7.895 0Z" fill="#FC8289"/><path d="M5 10.714c-.303.08-.845.28-.698.688.28.444.882.508 1.356.604a6.272 6.272 0 0 0 3.55-.535c-.377-.118-.73-.342-1.078-.479-1.013.207-2.094.294-3.102.023.052-.12.514-.396.128-.312L5 10.714Zm-.325-1.47c-.302.122-.84.266-.788.688.186.421.748.46 1.142.552 1.5.218 3.038.026 4.478-.423-.318-.119-.657-.231-.892-.489-1.276.253-2.624.38-3.9.11-.18-.094.184-.27.204-.366.36-.309-.125-.046-.244-.072Zm-1.818 3.104c.464-.309 1.036-.389 1.584-.313-.257-.186-.492-.397-.83-.35-.637.063-1.319.229-1.783.696-.23.27.096.58.373.612 2.354.443 4.808.508 7.173.095.617-.161 1.355-.232 1.802-.73.208-.354-.282-.612-.569-.635-.118.03.21.24.202.395-.29.32-.801.31-1.205.412-3 .39-5.964.234-6.747-.182Zm6.426-3.71c.23-.124.471-.221.66-.406-.742-.044-1.468.2-2.206.226-1.2.074-2.43.21-3.618-.017-.184-.043.15-.139.197-.176.427-.19.9-.232 1.311-.463-.17-.04-.336-.111-.514-.09-.77.044-1.564.233-2.207.663-.228.216.056.495.291.524 1.636.452 5.348.225 6.086-.261Zm1.232-1.053c-.39-.001-.764.185-.923.56-.183.248.306-.113.47-.11.52-.216 1.152.35.904.885-.257.649-.95.96-1.472 1.332-.434.356-.295.372.168.204.837-.245 1.842-.637 2.117-1.55.198-.75-.532-1.39-1.264-1.32Zm-7.283 5.736c.605.587 1.508.547 2.287.64 1.777.076 3.603.092 5.311-.443.488-.158 1.11-.542.974-1.149.04-.363-.143.115-.22.178-1.056 1.046-5.76 1.19-8.352.774Z" fill="#80CBC4"/></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h14v14H0z"/></clipPath></defs></svg>'
    ,".png":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><mask id="a" mask-type="alpha" maskUnits="userSpaceOnUse" x="1" y="3" width="14" height="10"><rect x="1.75" y="3" width="12.5" height="10" rx="2" fill="#00B6C2"/></mask><g mask="url(#a)"><path fill="#80CBC4" d="M1.75 3h12.5v10H1.75z"/><path d="M11.563 8 4.25 14.25l10.688-.446.562-4.018L11.562 8Z" fill="#343944"/><path d="M5.396 8.208a1.563 1.563 0 1 0 0-3.125 1.563 1.563 0 0 0 0 3.125Z" fill="#fff"/></g></svg>'
    ,".ttf":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 13v-.802l1.315-.078c.155-.01.185-.055.185-.22V4H3.094c-.121 0-.155.011-.177.122L2.741 5H2V3h8v2h-.74l-.177-.878C9.06 4.01 9.027 4 8.906 4H6.5v7.9c0 .154.02.198.185.21L8 12.197V13H4Z" fill="#F07178"/><path d="M9.5 13v-.802l.815-.078c.155-.01.185-.055.185-.22V7.5H9.094c-.121 0-.155.011-.177.122l-.176.878H8v-2h6v2h-.74l-.177-.878c-.022-.111-.056-.122-.177-.122H11.5v4.4c0 .154.02.198.185.21l.815.088V13h-3Z" fill="#9883EC"/></svg>'
    ,"":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path opacity=".8" d="M6.6 2H2.4c-.77 0-1.393.619-1.393 1.375L1 11.625C1 12.381 1.63 13 2.4 13h11.2c.77 0 1.4-.619 1.4-1.375V4.75c0-.756-.63-1.375-1.4-1.375H8L6.6 2Z" fill="#4A616C"/></svg>'
    ,".lnk":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 13.5S12 9 7.5 9v3L2 7l5.5-5v3C13 5 14 10 14 12v1.5Z" fill="#80CBC4"/></svg>'
    ,".exe":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="m8 6.31 4.895-2.183L8.22 2.055c-.165-.055-.33-.055-.44 0L3.105 4.127 8 6.31Z" fill="#89DDFF"/><path d="M8.55 7.236v6.546l4.62-2.018c.22-.11.33-.273.33-.491V5.055L8.55 7.236Zm-1.1 0L2.5 5.055v6.218c0 .218.11.436.33.49l4.62 2.019V7.236Z" fill="#82AAFF"/></svg>'
    ,".cpp":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="m7.87 10.269.231 1.394c-.147.08-.384.154-.7.223A5.09 5.09 0 0 1 6.263 12c-1.249-.023-2.187-.4-2.814-1.12-.633-.726-.95-1.646-.95-2.76.028-1.32.407-2.331 1.13-3.04C4.377 4.366 5.303 4 6.423 4c.424 0 .79.04 1.096.109.305.068.531.142.678.228L7.87 5.76l-.6-.194a3.214 3.214 0 0 0-.785-.086c-.656-.006-1.198.206-1.622.629-.43.417-.65 1.057-.667 1.908 0 .777.209 1.383.61 1.829.401.44.967.668 1.69.674l.752-.069c.243-.045.446-.108.622-.182Zm-.718-2.84h1.13V6.286h1.131v1.143h1.13V8.57h-1.13v1.143h-1.13V8.571h-1.13V7.43Zm5.087 0h-1.13V8.57h1.13v1.143h1.13V8.571H14.5V7.43h-1.13V6.286h-1.13v1.143Z" fill="#3965BD"/></svg>'
    ,".c":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="m11.51 11.403.347 2.091c-.22.12-.574.232-1.046.335A7.557 7.557 0 0 1 9.116 14c-1.864-.034-3.263-.6-4.2-1.68C3.973 11.231 3.5 9.851 3.5 8.18c.042-1.98.607-3.497 1.687-4.56C6.3 2.549 7.683 2 9.352 2c.633 0 1.18.06 1.636.163.456.103.793.214 1.012.343l-.49 2.134-.893-.291a4.77 4.77 0 0 0-1.172-.129c-.978-.009-1.788.309-2.42.943-.641.626-.97 1.586-.995 2.863 0 1.165.312 2.074.91 2.743.6.66 1.442 1.002 2.522 1.011l1.121-.103a4.46 4.46 0 0 0 .928-.274Z" fill="#3965BD"/></svg>'
    ,".bat":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 4V2.5H2.5A.5.5 0 0 0 2 3v1h2Zm10 0V3a.5.5 0 0 0-.5-.5H5V4h9Z" fill="#89DDFF"/><path fill-rule="evenodd" clip-rule="evenodd" d="M2 5v8a.5.5 0 0 0 .5.5h11a.5.5 0 0 0 .5-.5V5H2Zm4.354 4.354L4.5 11.207l-.707-.707 1.5-1.5-1.5-1.5.707-.707 1.854 1.853a.5.5 0 0 1 0 .707ZM7.5 11h3v-1h-3v1Z" fill="#3965BD"/></svg>'
    ,".txt":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 3h5l2 1 1 2v7H4V3Z" fill="#A9B4CB"/><path fill-rule="evenodd" clip-rule="evenodd" d="M9 2a1 1 0 0 1 .707.293l3 3A1 1 0 0 1 13 6v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h4Zm3 4v6a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h4l3 3Z" fill="#A9B4CB"/><path d="M9 3v3h3" fill="#F5F7F9"/><path d="M10 8.5H6m4 2H6" stroke="#434F65" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 6.5H6" stroke="#252D3A" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    ,".md":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M8.87 10.71H7.13V8L5.814 9.733 4.5 8.001v2.708H2.76V5.293H4.5l1.315 1.812L7.13 5.293h1.74v5.416Zm2.611.437L9.316 8h1.315V5.292h1.74V8h1.316l-2.204 3.147h-.002ZM13.995 3.5H2.005a.952.952 0 0 0-.705.308c-.2.206-.3.448-.3.727v6.93a1 1 0 0 0 .3.737c.2.199.434.298.705.298h11.99c.27 0 .506-.1.706-.298a.998.998 0 0 0 .299-.737v-6.93c0-.279-.1-.521-.3-.727a.952.952 0 0 0-.705-.308Z" fill="#F78C6C"/></svg>'
    ,".py":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><g fill-rule="evenodd" clip-rule="evenodd"><path d="M11.703 5.796h-.856v1.309s.046 1.561-1.41 1.561h-2.43s-1.365-.024-1.365 1.437v2.416c-.21 1.9 4.924 1.96 4.882.249l-.003-1.256H8.07v-.377h3.423c2.25.188 2.107-5.418.209-5.34ZM9.247 13.07a.502.502 0 0 1 0-.83c.293-.185.661.047.661.415s-.368.6-.661.415Z" fill="#FFCB6B"/><path d="M4.458 11.21h.856V9.9s-.046-1.56 1.41-1.56h2.43s1.365.024 1.365-1.437V4.294c-.217-1.79-5.039-1.648-4.882-.036v1.235h2.452v.377H4.667c-2.311-.053-2.064 5.34-.209 5.34Zm2.014-6.445a.502.502 0 0 1 0-.831c.293-.184.662.047.662.415s-.369.6-.662.416Z" fill="#89DDFF"/></g></svg>'
    ,".xml":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M12.5 11V3.5A1.5 1.5 0 0 0 11 2H3.75A1.75 1.75 0 0 0 2 3.75V5h2.5v7.5A1.5 1.5 0 0 0 6 14h6.25A1.75 1.75 0 0 0 14 12.25V11h-1.5ZM3 4v-.25a.75.75 0 0 1 1.5 0V4H3Zm7 1.793-.707.707 1 1-1 1 .707.707 1.354-1.354a.5.5 0 0 0 0-.707L10 5.793Zm-3.854 2.06a.5.5 0 0 1 0-.707L7.5 5.793l.707.707-1 1 1 1-.707.707-1.354-1.354ZM12.25 13a.75.75 0 0 0 .75-.75V12H8v.25c0 .293-.061.54-.162.75h4.412Z" fill="#C3E88D"/></svg>'
    ,".un":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M8.083 2.167H4.5a1.167 1.167 0 0 0-1.167 1.166v9.334A1.166 1.166 0 0 0 4.5 13.833h7a1.167 1.167 0 0 0 1.167-1.166V6.75H8.583a.5.5 0 0 1-.5-.5V2.167Zm4.084 3.583L9.083 2.667V5.75h3.084Z" fill="#697DA5"/></svg>'
    ,".ts":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M13 4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4Zm-4.13 6.655-.203.736c.125.06.298.115.52.167.223.052.459.078.708.078.592 0 1.03-.121 1.314-.364.285-.243.427-.531.427-.863 0-.283-.09-.52-.272-.71-.182-.192-.466-.351-.85-.48a3.674 3.674 0 0 1-.61-.26c-.126-.075-.188-.174-.188-.298 0-.104.052-.195.155-.272.103-.076.26-.115.472-.115.211 0 .393.023.545.067a2.8 2.8 0 0 1 .358.127l.22-.722a2.706 2.706 0 0 0-.468-.141 3.029 3.029 0 0 0-.639-.06c-.51 0-.911.115-1.204.343-.293.228-.44.51-.44.848 0 .287.11.526.33.717.22.191.508.346.866.465.26.08.447.162.558.246.11.084.166.186.166.305a.362.362 0 0 1-.175.312c-.116.08-.286.12-.508.12a2.41 2.41 0 0 1-.607-.075 2.292 2.292 0 0 1-.475-.17v-.002.001ZM6.54 8.238v3.398h.862V8.238h1.265v-.693H5.273v.693H6.54Z" fill="#3965BD"/></svg>'
    ,".cs":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M4.474 12.571h1.743l.465-2.522h1.743l-.465 2.522h1.744l.465-2.522h1.898v-1.3h-1.588l.31-1.576h1.782v-1.3h-1.55l.504-2.444H9.82l-.503 2.444H7.573l.504-2.444H6.334l-.465 2.444H3.97v1.3h1.628l-.31 1.576h-1.86v1.3h1.55l-.504 2.522ZM8.736 8.75H6.993l.31-1.576h1.743l-.31 1.576Z" fill="#89DDFF"/></svg>'
    ,".mp3":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M14 8A6 6 0 1 1 2 8a6 6 0 0 1 12 0ZM8.6 5.025c.687.084 2.372.474 2.984 2.279a.3.3 0 0 1-.437.354c-.768-.454-1.992-.54-2.547-.556V10.1c0 .827-.673 1.5-1.5 1.5s-1.5-.673-1.5-1.5.673-1.5 1.5-1.5c.339 0 .649.117.9.308V4.4h.6v.625Z" fill="#FC8289"/></svg>'
    ,".mp4":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M3 5.5h10a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-.5.5H3a.5.5 0 0 1-.5-.5V6a.5.5 0 0 1 .5-.5Zm7 4-3.5-2v4l3.5-2Z" fill="#FC8289"/><path d="M2.11 4.14a.5.5 0 0 1 .39-.59l9.652-1.969a.5.5 0 1 1 .2.98L2.7 4.53a.5.5 0 0 1-.59-.39Z" fill="#FFCB6B"/></svg>'
    ,".pdf":'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="32" height="32" viewBox="0 0 32 32"><path fill="#909090" d="m24.1 2.072l5.564 5.8v22.056H8.879V30h20.856V7.945L24.1 2.072"></path><path fill="#f4f4f4" d="M24.031 2H8.808v27.928h20.856V7.873L24.03 2"></path><path fill="#7a7b7c" d="M8.655 3.5h-6.39v6.827h20.1V3.5H8.655"></path><path fill="#dd2025" d="M22.472 10.211H2.395V3.379h20.077v6.832"></path><path fill="#464648" d="M9.052 4.534H7.745v4.8h1.028V7.715L9 7.728a2.042 2.042 0 0 0 .647-.117a1.427 1.427 0 0 0 .493-.291a1.224 1.224 0 0 0 .335-.454a2.13 2.13 0 0 0 .105-.908a2.237 2.237 0 0 0-.114-.644a1.173 1.173 0 0 0-.687-.65a2.149 2.149 0 0 0-.409-.104a2.232 2.232 0 0 0-.319-.026m-.189 2.294h-.089v-1.48h.193a.57.57 0 0 1 .459.181a.92.92 0 0 1 .183.558c0 .246 0 .469-.222.626a.942.942 0 0 1-.524.114m3.671-2.306c-.111 0-.219.008-.295.011L12 4.538h-.78v4.8h.918a2.677 2.677 0 0 0 1.028-.175a1.71 1.71 0 0 0 .68-.491a1.939 1.939 0 0 0 .373-.749a3.728 3.728 0 0 0 .114-.949a4.416 4.416 0 0 0-.087-1.127a1.777 1.777 0 0 0-.4-.733a1.63 1.63 0 0 0-.535-.4a2.413 2.413 0 0 0-.549-.178a1.282 1.282 0 0 0-.228-.017m-.182 3.937h-.1V5.392h.013a1.062 1.062 0 0 1 .6.107a1.2 1.2 0 0 1 .324.4a1.3 1.3 0 0 1 .142.526c.009.22 0 .4 0 .549a2.926 2.926 0 0 1-.033.513a1.756 1.756 0 0 1-.169.5a1.13 1.13 0 0 1-.363.36a.673.673 0 0 1-.416.106m5.08-3.915H15v4.8h1.028V7.434h1.3v-.892h-1.3V5.43h1.4v-.892"></path><path fill="#dd2025" d="M21.781 20.255s3.188-.578 3.188.511s-1.975.646-3.188-.511Zm-2.357.083a7.543 7.543 0 0 0-1.473.489l.4-.9c.4-.9.815-2.127.815-2.127a14.216 14.216 0 0 0 1.658 2.252a13.033 13.033 0 0 0-1.4.288Zm-1.262-6.5c0-.949.307-1.208.546-1.208s.508.115.517.939a10.787 10.787 0 0 1-.517 2.434a4.426 4.426 0 0 1-.547-2.162Zm-4.649 10.516c-.978-.585 2.051-2.386 2.6-2.444c-.003.001-1.576 3.056-2.6 2.444ZM25.9 20.895c-.01-.1-.1-1.207-2.07-1.16a14.228 14.228 0 0 0-2.453.173a12.542 12.542 0 0 1-2.012-2.655a11.76 11.76 0 0 0 .623-3.1c-.029-1.2-.316-1.888-1.236-1.878s-1.054.815-.933 2.013a9.309 9.309 0 0 0 .665 2.338s-.425 1.323-.987 2.639s-.946 2.006-.946 2.006a9.622 9.622 0 0 0-2.725 1.4c-.824.767-1.159 1.356-.725 1.945c.374.508 1.683.623 2.853-.91a22.549 22.549 0 0 0 1.7-2.492s1.784-.489 2.339-.623s1.226-.24 1.226-.24s1.629 1.639 3.2 1.581s1.495-.939 1.485-1.035"></path><path fill="#909090" d="M23.954 2.077V7.95h5.633l-5.633-5.873Z"></path><path fill="#f4f4f4" d="M24.031 2v5.873h5.633L24.031 2Z"></path><path fill="#fff" d="M8.975 4.457H7.668v4.8H8.7V7.639l.228.013a2.042 2.042 0 0 0 .647-.117a1.428 1.428 0 0 0 .493-.291a1.224 1.224 0 0 0 .332-.454a2.13 2.13 0 0 0 .105-.908a2.237 2.237 0 0 0-.114-.644a1.173 1.173 0 0 0-.687-.65a2.149 2.149 0 0 0-.411-.105a2.232 2.232 0 0 0-.319-.026m-.189 2.294h-.089v-1.48h.194a.57.57 0 0 1 .459.181a.92.92 0 0 1 .183.558c0 .246 0 .469-.222.626a.942.942 0 0 1-.524.114m3.67-2.306c-.111 0-.219.008-.295.011l-.235.006h-.78v4.8h.918a2.677 2.677 0 0 0 1.028-.175a1.71 1.71 0 0 0 .68-.491a1.939 1.939 0 0 0 .373-.749a3.728 3.728 0 0 0 .114-.949a4.416 4.416 0 0 0-.087-1.127a1.777 1.777 0 0 0-.4-.733a1.63 1.63 0 0 0-.535-.4a2.413 2.413 0 0 0-.549-.178a1.282 1.282 0 0 0-.228-.017m-.182 3.937h-.1V5.315h.013a1.062 1.062 0 0 1 .6.107a1.2 1.2 0 0 1 .324.4a1.3 1.3 0 0 1 .142.526c.009.22 0 .4 0 .549a2.926 2.926 0 0 1-.033.513a1.756 1.756 0 0 1-.169.5a1.13 1.13 0 0 1-.363.36a.673.673 0 0 1-.416.106m5.077-3.915h-2.43v4.8h1.028V7.357h1.3v-.892h-1.3V5.353h1.4v-.892"></path></svg>'
    ,".download":'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24" height="24" viewBox="0 0 24 24"><path fill="#1A55E8" d="m12 16l-5-5l1.4-1.45l2.6 2.6V4h2v8.15l2.6-2.6L17 11Zm-8 4v-5h2v3h12v-3h2v5Z"></path></svg>'
    ,".db":'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24" height="24" viewBox="0 0 24 24"><path fill="#ECC849" d="M21 16v3c0 1.657-4.03 3-9 3s-9-1.343-9-3v-3c0 1.657 4.03 3 9 3s9-1.343 9-3Zm-9-1c-4.97 0-9-1.343-9-3v3c0 1.657 4.03 3 9 3s9-1.343 9-3v-3c0 1.657-4.03 3-9 3Zm0-13C7.03 2 3 3.343 3 5v2c0 1.657 4.03 3 9 3s9-1.343 9-3V5c0-1.657-4.03-3-9-3Zm0 9c-4.97 0-9-1.343-9-3v3c0 1.657 4.03 3 9 3s9-1.343 9-3V8c0 1.657-4.03 3-9 3Z"></path></svg>'
    ,".apk":'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24" height="24" viewBox="0 0 24 24"><path fill="#0BB978" d="M7 19h10q-.1-1.225-.75-2.25t-1.7-1.625l.95-1.7q.05-.1.025-.225t-.15-.175q-.1-.05-.212-.025q-.113.025-.163.125l-.975 1.75q-.5-.2-1-.313q-.5-.112-1.025-.112q-.525 0-1.025.112q-.5.113-1 .313L9 13.125Q8.95 13 8.838 13q-.113 0-.238.05l-.1.375l.95 1.7q-1.05.6-1.7 1.625Q7.1 17.775 7 19Zm2.75-1.5q-.2 0-.35-.15q-.15-.15-.15-.35q0-.2.15-.35q.15-.15.35-.15q.2 0 .35.15q.15.15.15.35q0 .2-.15.35q-.15.15-.35.15Zm4.5 0q-.2 0-.35-.15q-.15-.15-.15-.35q0-.2.15-.35q.15-.15.35-.15q.2 0 .35.15q.15.15.15.35q0 .2-.15.35q-.15.15-.35.15ZM6 22q-.825 0-1.412-.587Q4 20.825 4 20V4q0-.825.588-1.413Q5.175 2 6 2h7.175q.4 0 .763.15q.362.15.637.425l4.85 4.85q.275.275.425.637q.15.363.15.763V20q0 .825-.587 1.413Q18.825 22 18 22Zm7-14q0 .425.288.712Q13.575 9 14 9h4l-5-5Z"></path></svg>'
    }
def get_icons(ex:str):
    ex = ex.lower()
    if ex in ['.zip','.rar','.7z','.iso','.gz','.zip','.zip']:
        return icons[".zip"]
    elif ex in ['.exe']:
        return icons[".exe"]
    elif ex in ['.doc','.docx']:
        return icons[".doc"]
    elif ex in ['.ico','.png','.gif','.jpg','.jpeg','.zip','.zip']:
        return icons[".png"]
    elif ex in ['.mp3','.ogg','.wav','.mid']:
        return icons[".mp3"]
    elif ex in ['.mp4','.avi','.flv','.rmvb']:
        return icons[".mp4"]
    elif ex in icons:
        return icons[ex]
    else:
        return icons[".un"]

class BaseHeader:
    def __init__(self) -> None:
        self.headers = {}
        self.Content_Type = ""
        self.Content_Length = ""
        self.Content_Encoding = ""
        self.ContentLanguage = ""

class Request(BaseHeader):
    def __init__(self,recv_client_content:str) -> None:
        super().__init__()
        self.Params = {}
        first = recv_client_content.split(" ", maxsplit=3)
        if (len(first) > 0):
            self.method = first[0]
        if (len(first)  > 1):
            self.url = first[1]
        if (len(first)  > 2):
            self.protocol_version = first[2]

class Response(BaseHeader):
    def __init__(self,socket) -> None:
        super().__init__()
        self.socket = socket
        self.line = bytes()
        self.body = bytes()
    def _build_header(self):
        key_list = self.headers.keys()
        # print(list(key_list))
        h = ""
        for key in key_list:
            h += f"{key}:{self.headers[key]}"
        return h+'\r\n'
    def setLine(self,line:str):
        self.line = line.encode("utf-8")
    def setBody(self,body:str):
        if isinstance(body,bytes):
            self.body = body
        else :
            self.body = body.encode("utf-8")
    def _toBytes(self):
        return self.line + self._build_header().encode("utf-8") + self.body
    def send(self):
        self.socket.send(self._toBytes())
        self.socket.close()

class HttpWebServer(object):
    def __init__(self,ip = "0.0.0.0",port = 80,static_path = 'static'):
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        tcp_server_socket.bind((ip, port))
        tcp_server_socket.listen(128)

        self.tcp_server_socket = tcp_server_socket
        self.staticPath = static_path
        print(f'Static path is "{static_path}"')
        print(f'Server runing on "http://{ip}{(":"+str(port)) if port != 80 else ""}/"')

    def handle_client_request(self,new_socket:socket):
        recv_client_data = new_socket.recv(4096)
        if len(recv_client_data) == 0:
            new_socket.close()
            return
        recv_client_content = recv_client_data.decode("utf-8")
        request = Request(recv_client_content)
        response = Response(new_socket)
        if request.method == 'GET':
            response_data = self.on_get(request,response)
        elif request.method == 'POST':
            response_data = self.on_post(request,response)
        else:
            response_data = self.on_default(request,response)
    def on_default(self,request:Request,response:Response):
        response.setLine("HTTP/1.1 200 OK\r\n")
        response.headers["Content-Type"]= "text/html; charset=UTF-8\r\n"
        response.headers["Server"] = "jj_file_server\r\n"
        response.headers["Access-Control-Allow-Origin"] = "*\r\n"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS\r\n"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Access-Control-Allow-Headers, Access-Control-Request-Headers, Access-Control-Request-Method, Authorization, X-Requested-With, User-Agent, Referer, Origin\r\n"
        response.send()
    
    def on_post(self,request:Request,response:Response):
        pass
    def on_get(self,request:Request,response:Response):
        try:
            result = urllib.parse.urlsplit(request.url)
            query = dict(urllib.parse.parse_qsl(result.query))
            dir = urllib.parse.unquote(self.staticPath + str(result.path))
            if(not os.path.exists(dir)):
                if result.path != '/favicon.ico':
                    raise "无效路径!"
            dir_list = []
            if(os.path.isdir(dir)):
                dir_list = os.listdir(dir)
                if 'index.html' in dir_list:
                    dir += "/index.html"
            if os.path.isdir(dir):
                dir_list.sort(key=lambda x:os.path.splitext(x)[-1])
                response.setLine("HTTP/1.1 200 OK\r\n")
                response.headers["Content-Type"]= "text/html; charset=UTF-8\r\n"
                fileListStr = ""
                if len(request.url) > 1:
                    t = os.path.join(request.url,"../")
                    fileListStr += f'<li><a href=\"{t}\">../</a></li>'
                for l in dir_list:
                    t = urllib.parse.quote(os.path.join("./",request.url,l), safe='/:\\')
                    ex = os.path.splitext(l)[-1]
                    fileListStr += f'''
                    <li >
                        <span>
                            {get_icons(ex)}
                            {f"<img style = 'height:16px;' src = '{t}' />" if ex =='.svg' else ""}
                            &nbsp;
                            <a href='{t}'>{l}</a>
                        </span>
                        {"" if ex =='' else f"<a href='{t+'?download=true'}' style='min-width:32px'>{get_icons('.download')}</a>"}
                    </li>
                    '''
                response.setBody(f"""
                <!DOCTYPE html>
                <html lang="zh-cn">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="icon" href="./server.ico">
                    <title>fileserver</title>
                    <style>
                        *{{
                            padding:0;
                            margin:0;
                            font-size:16px;
                            color:#1A55E8;
                        }}
                        body{{
                            padding:20px 0;
                        }}
                        a{{
                            text-decoration:none;
                        }}
                        svg{{
                            vertical-align: text-bottom;
                            width: 16px;
                            height: 16px;
                        }}
                        ul li:nth-child(odd) {{
                            background-color:#BCCEFB30;
                        }}
                        /*ul li:nth-child(even) {{
                            background-color:#fff;
                        }}*/
                        ul>li{{
                            display: flex;
                            align-items: 
                            center;justify-content: 
                            space-between;
                            padding:0 10px;
                        }}
                        ul>li:hover{{
                            background-color:#F5979430;
                            color:#333333;
                        }}
                    </style>
                </head>
                <body>
                    <div style ="width:90%;margin:auto;">
                        <h1>{urllib.parse.unquote(request.url)}</h1>
                        <ul>{fileListStr}</ul>
                    </div>
                </body>
                </html>
                """)
            elif os.path.isfile(dir):
                response.setLine("HTTP/1.1 200 OK\r\n")
                ex = os.path.splitext(dir)[-1]
                if "download" in query:
                    response.headers["Content-Type"]= "application/octet-stream\r\n"
                elif ex == '.js':
                    response.headers["Content-Type"]= "application/x-javascript\r\n"
                elif ex == '.ico':
                    response.headers["Content-Type"]= "image/x-icon\r\n"
                elif ex == '.svg':
                    response.headers["Content-Type"]= "image/svg+xml\r\n"
                elif ex == '.css':
                    response.headers["Content-Type"]= "text/css\r\n"
                elif ex in '.html':
                    response.headers["Content-Type"]= "text/html; charset=UTF-8\r\n"
                else:
                    response.headers['Content-type'] = "text/plain; charset=UTF-8\r\n"

                if result.path == '/favicon.ico' and not os.path.exists(dir):
                    response.body = favicon
                    response.headers["Content-Length"]= f"{len(response.body)}\r\n"
                else:
                    with open(dir, "rb") as file:
                        response.body = file.read()
                        response.headers["Content-Length"]= f"{len(response.body)}\r\n"
        except Exception as e:
            print(f"{urllib.parse.unquote(request.url)} {type(e)}:{e}")
            response.setLine("HTTP/1.1 404 Not Found\r\n")
            response.setBody(f"""
            <!DOCTYPE html>
            <html lang="zh-cn">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <link rel="icon" href="./server.ico">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>404</title>
                <style>
                h1{
                text-align: center
                }
                h3{
                text-align: center
                }
                </style>
            </head>
            <body>
                <h1>404</h1>
                <h3>{e}</h3>
            </body>
            </html>
            """)
        finally:
            # response.headers["Access-Control-Allow-Origin"] = "*\r\n"
            # response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS\r\n"
            # response.headers["Access-Control-Allow-Headers"] = "Content-Type, Access-Control-Allow-Headers, Access-Control-Request-Headers, Access-Control-Request-Method, Authorization, X-Requested-With, User-Agent, Referer, Origin\r\n"
            response.send()

    def start(self):
        while True:
            new_socket, ip_port = self.tcp_server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client_request, args=(new_socket,))
            client_thread.daemon = True
            client_thread.start()
    def start_async(self):
        server_thread = threading.Thread(name="fileserver",target=self.start)
        server_thread.start()


if __name__ == '__main__':
    dir = os.getcwd()
    # dir = os.path.dirname(os.path.realpath(__file__)) 
    if len(sys.argv)>1 and os.path.isdir(sys.argv[1]):
        dir = sys.argv[1]
    web_server = HttpWebServer(socket.gethostbyname(socket.gethostname()),80,dir)
    web_server.start_async()

