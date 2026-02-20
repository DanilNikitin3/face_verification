import { CameraView, CameraType, useCameraPermissions, BarcodeScanningResult } from 'expo-camera';
import { setStatusBarBackgroundColor } from 'expo-status-bar';
import { useState, useRef, useEffect } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View, Image, Alert } from 'react-native';

export default function App() {
  const [permission, requestPermission] = useCameraPermissions();
  const [imageUri, setImageUri] = useState(null);
  const cameraRef = useRef(null);
  const [message, setMessage] = useState(null);
  const [scanned, setScanned] = useState(null);
  const [data, setData] = useState(null);
  const [cameradata, ChangeCamera] = useState('back');

  // const handlePress = () => {
  //   takePicture()
  //   sendData();
  // };

  const takePicture = async () => {
    if (cameraRef.current) {
      ChangeCamera('front');

      const photo = await cameraRef.current.takePictureAsync({ quality: 0.5 });
      console.log(photo.uri);
      setImageUri(photo.uri);

      await sendPhoto(photo.uri)

      ChangeCamera('back');
    }
  };

  const handleBarCodeScanned = ({ type, data }) => {
    if (scanned) return; 

    console.log('QR отсканирован:', data, 'Тип:', type);

    if (data === 'test') {
      setScanned(true);  

      setData(data);    

      // Alert.alert(
      //   'QR-код отсканирован!',
      //   `Данные: ${data}\nТип: ${type}`,
      //   [
      //     {
      //       text: 'OK',
      //       onPress: () => {
      //         setScanned(false);  
      //       },
      //     },
      //   ]
      // );

      setScanned(false);

    } else {
      console.log('QR не тест:', data);
    }
  };

  const sendPhoto = async (photoUri) => {   
    if (!photoUri) {
      console.log("Нет фото");
      return;
    }

    const fileName = photoUri.split('/').pop() || `photo_${Date.now()}.jpg`;

    const formData = new FormData();
    
    formData.append('photo', {   
      uri: photoUri,
      name: fileName,
      type: 'image/jpeg',        
    });

    try {
      const response = await fetch('http://192.168.99.18:5000/upload-photo', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Ошибка сервера: ${response.status}`);
      }

      const result = await response.json();
      setMessage(result.message || 'Фото успешно отправлено и обработано');
      console.log('Ответ сервера:', result);

    } catch (error) {
      console.error('Ошибка при отправке фото:', error);
      setMessage('Не удалось отправить фото');
    }
  };

  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={{ textAlign: 'center' }}>We need your permission to show the camera</Text>
        <Button onPress={requestPermission} title="Grant Permission" />
      </View>
    );
  }

  // return (
  //   <View style={styles.container}>
  //     {imageUri ? (
  //       <View style={styles.previewContainer}>
  //         <Image source={{ uri: imageUri }} style={styles.previewImage} />
  //         <TouchableOpacity style={styles.button} onPress={() => setImageUri(null)}>
  //           <Text style={styles.text}>Retake Picture</Text>
  //         </TouchableOpacity>
  //       </View>
  //     ) : (
  //       <CameraView 
  //         style={styles.camera} 
  //         facing="back"
  //         ref={cameraRef}
  //       >
  //         <View style={styles.buttonContainer}>
  //           <TouchableOpacity style={styles.button} onPress={takePicture}>
  //             <Text style={styles.text}>Take Photo</Text>
  //           </TouchableOpacity>
  //         </View>
  //       </CameraView>
  //     )}
  //   </View>
  // );

  return (
    <View style={styles.container}>
      <CameraView
        ref={cameraRef}
        style={styles.camera}
        facing={cameradata}
        onBarcodeScanned={scanned ? undefined : handleBarCodeScanned}
        barcodeScannerSettings={{
          barcodeTypes: ['qr'],
        }}
      />

      {data === 'test' && (
        <View style={styles.overlay}>
          <TouchableOpacity
            style={styles.captureButton}
            onPress={async () => {
              await takePicture();           
              setData(null);               
              setScanned(false);             
            }}
          >
            <Text style={styles.buttonText}>Сделать фото и отправить</Text>
          </TouchableOpacity>

          <Text style={styles.overlayText}>QR "test" найден! Нажмите, чтобы сфотографировать</Text>
        </View>
      )}

      {imageUri && (
        <View style={styles.previewOverlay}>
          <Image source={{ uri: imageUri }} style={styles.previewImage} />
          <TouchableOpacity onPress={() => setImageUri(null)}>
            <Text style={{ color: 'white' }}>Закрыть превью</Text>
            <Text style={{ color: 'white' }}>Получено фото - {message}</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  camera: {
    flex: 1,
    width: '100%',
  },
  overlay: {
    ...StyleSheet.absoluteFillObject,  
    justifyContent: 'flex-end',
    alignItems: 'center',
    paddingBottom: 80,                 
    backgroundColor: 'rgba(0,0,0,0.4)',
  },
  captureButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 30,
    elevation: 5,
    shadowColor: '#000',
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  overlayText: {
    color: 'white',
    fontSize: 16,
    marginTop: 20,
    textAlign: 'center',
  },
  previewOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0,0,0,0.8)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  previewImage: {
    width: '90%',
    height: '70%',
    borderRadius: 12,
  },
});



