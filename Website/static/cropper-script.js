const imageInput = document.getElementById('imageInput');
const imagePreview = document.getElementById('imagePreview');
const saveButton = document.getElementById('saveButton');

let cropper;

imageInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      const imageUrl = event.target.result;
      imagePreview.src = imageUrl;

      if (cropper) {
        cropper.destroy();
      }

      cropper = new Cropper(imagePreview, {
        aspectRatio: 1, // Square aspect ratio
        viewMode: 2,    // Display the cropped area in the center
        dragMode: 'move', // Allow users to move the cropped area
      });
    };

    reader.readAsDataURL(file);
  }
});

saveButton.addEventListener('click', () => {
  if (cropper) {
    const croppedCanvas = cropper.getCroppedCanvas();
    const croppedImageUrl = croppedCanvas.toDataURL();

    // You can now use 'croppedImageUrl' to save, display, or manipulate the cropped image.
    // For example, you could set it as the source of an <img> element or send it to a server.
    console.log('Cropped Image URL:', croppedImageUrl);
  }
});
