const developerKey = '';
const clientId = '';
const scope = 'https://www.googleapis.com/auth/drive.file ' +
    'https://www.googleapis.com/auth/drive.metadata ' +
    'https://www.googleapis.com/auth/drive.readonly';
let GoogleAuth;
let access_token;

let IMAGE_BASE64;
let IMAGE_TYPE;
let IMAGE_FILENAME;

const signOutBtn = document.getElementById('googleDriveSignOut');
const authBtn = document.getElementById('googleDriveChoose');

// ===== start function ===== //
function onApiLoad() {

    gapi.load('auth2', function() {

        auth2 = gapi.auth2.init({
            client_id: clientId,
            prompt: 'select_account',
            scope: scope
        }).then(function() {

            GoogleAuth = gapi.auth2.getAuthInstance();
            if (gapi.auth2.getAuthInstance().isSignedIn.get()) {
                // signOutBtn.classList.remove("invisible");
            }
            onAuthApiLoad()
        });
    });
}

function onAuthApiLoad() {
    const signOutBtn = document.getElementById('googleDriveSignOut');
    const authBtn = document.getElementById('googleDriveChoose');

    authBtn.addEventListener('click', function() {

        if (!gapi.auth2.getAuthInstance().isSignedIn.get()) {

            GoogleAuth.grantOfflineAccess({
                prompt: 'select_account', //select_account, consent
                scope: scope
            }).then(
                function(resp) {
                    reloadUserAuth();
                }
            );
        } else {
            reloadUserAuth();
        }
    });

    signOutBtn.addEventListener('click', function() {
        GoogleAuth.signOut();
        signOutBtn.classList.add("invisible");
    });
}

function reloadUserAuth() {
    const signOutBtn = document.getElementById('googleDriveSignOut');

    googleUser = GoogleAuth.currentUser.get();
    googleUser.reloadAuthResponse().then(
        function(authResponse) {
            signOutBtn.classList.remove("invisible");
            access_token = authResponse.access_token;
            createPicker(authResponse);
        }
    );
}

function createPicker(authResult) {

    if (authResult && !authResult.error) {

        gapi.load('picker', function() {
            const picker = new google.picker.PickerBuilder().
            enableFeature(google.picker.Feature.MULTISELECT_ENABLED).
            // addView(google.picker.ViewId.DOCS). // all types
            addView(google.picker.ViewId.DOCS_IMAGES).
            setOAuthToken(access_token).
            setDeveloperKey(developerKey).
            setCallback(pickerCallback).
            build();
            picker.setVisible(true);
        });
    }
}

async function pickerCallback(_data) {
    console.log(_data)
    files = _data[google.picker.Response.DOCUMENTS];
    if (files) {
        const xhrArray = _data[google.picker.Response.DOCUMENTS].map(async doc => {
            const result = await getPhotoMetadata(`https://www.googleapis.com/drive/v2/files/${doc.id}?key=${developerKey}`);
            downloadPhoto(result, onDownloadPhoto);
        });
        await Promise.all(xhrArray);
    }
}

function getPhotoMetadata(url) {
    return fetch(url, {
            headers: {
                "Authorization": `Bearer ${access_token}`,
                "Accept": "application/json"
            },
            method: 'GET'
        })
        .then(function(response) {
            if (response.ok) {
                return response.json();
            }
            return response.json();
        });
}

function downloadPhoto(file, callback) {
    console.log("FILE METADATA", file)

    IMAGE_FILENAME = file.originalFilename;
    IMAGE_EXT = file.fileExtension;
    IMAGE_TYPE = file.mimeType;

    if (file.downloadUrl) {
        var accessToken = gapi.auth.getToken().access_token;
        var xhr = new XMLHttpRequest();
        xhr.open('GET', file.downloadUrl);
        xhr.setRequestHeader('Authorization', 'Bearer ' + access_token);
        xhr.responseType = 'arraybuffer';
        xhr.onload = function() {
            callback(xhr.response);
        };
        xhr.onerror = function() {
            callback(null);
        };
        xhr.send();
    } else {
        callback(null);
    }
}

function onDownloadPhoto(response) {
    if (!response) {
        console.log("[ERROR]: Cannot download the file!")
        return;
    }
    console.log(`[SUCCESS]: Downloaded photo, ${IMAGE_FILENAME}`);
    IMAGE_BASE64 = `data:${IMAGE_TYPE};base64,` + base64ArrayBuffer(response);
    $("#image_test").attr("src", IMAGE_BASE64);
    uploadPhoto('/upload', IMAGE_BASE64);
}

function uploadPhoto(url = '/upload', data = {}) {
    if (!IMAGE_BASE64) {
        return;
    };

    parameters = {
        image_ext: IMAGE_EXT,
        image_name: IMAGE_FILENAME,
    };

    if (parameters) {
        url += '?';
        for (const property in parameters) {
            url += `${property}=${parameters[property]}&`
        }
    }

    console.log(url)

    return fetch(url, {
            method: "POST",
            body: data,
        })
        .then(function(response) {
            if (response.ok) {
                return response.json();
                // fix answer on server side
            }
            return response.text();
        });
}


function base64ArrayBuffer(arrayBuffer) {
    var base64 = ''
    var encodings = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    var bytes = new Uint8Array(arrayBuffer)
    var byteLength = bytes.byteLength
    var byteRemainder = byteLength % 3
    var mainLength = byteLength - byteRemainder
    var a, b, c, d
    var chunk
    for (var i = 0; i < mainLength; i = i + 3) {
        chunk = (bytes[i] << 16) | (bytes[i + 1] << 8) | bytes[i + 2]
        a = (chunk & 16515072) >> 18 // 16515072 = (2^6 - 1) << 18
        b = (chunk & 258048) >> 12 // 258048   = (2^6 - 1) << 12
        c = (chunk & 4032) >> 6 // 4032     = (2^6 - 1) << 6
        d = chunk & 63 // 63       = 2^6 - 1
        base64 += encodings[a] + encodings[b] + encodings[c] + encodings[d]
    }
    if (byteRemainder == 1) {
        chunk = bytes[mainLength]
        a = (chunk & 252) >> 2 // 252 = (2^6 - 1) << 2
        b = (chunk & 3) << 4 // 3   = 2^2 - 1
        base64 += encodings[a] + encodings[b] + '=='
    } else if (byteRemainder == 2) {
        chunk = (bytes[mainLength] << 8) | bytes[mainLength + 1]
        a = (chunk & 64512) >> 10 // 64512 = (2^6 - 1) << 10
        b = (chunk & 1008) >> 4 // 1008  = (2^6 - 1) << 4
        c = (chunk & 15) << 2 // 15    = 2^4 - 1
        base64 += encodings[a] + encodings[b] + encodings[c] + '='
    }
    return base64
}