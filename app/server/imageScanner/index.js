import ImageKit from 'imagekit';
import axios from 'axios';
const imagekit = new ImageKit({
  publicKey: 'public_UghEp/T158eyYtp7mtkhVRQkrew=',
  privateKey: 'private_216cw3c0/5sUx2KW5VJ3ELqRfgM=',
  urlEndpoint: 'https://ik.imagekit.io/4rp923pit',
});

Meteor.methods({
  uploadImage(file) {
    return imagekit.upload({
      file,
      fileName: `${+new Date()}-scannedimage.jpg`,
      extensions: [
        {
          name: 'google-auto-tagging',
          maxTags: 5,
          minConfidence: 95,
        },
      ],
    });
  },
  getAIResponseForScannedImage(imageURL) {
    return new Promise(function (resolve, reject) {
      axios(`${Meteor.settings.public.ROOT_URL_IMAGE_SCANNING}/imageRecognition?imageURL=${imageURL}`, {
        method: 'POST',
      })
        .then(result => {
          if (result?.data) {
            resolve(result.data);
          } else {
            reject();
          }
        })
        .catch(error => {
          reject(error);
        });
    });
  },
});
