import numpy as np
import vmlab_py
import librosa




if __name__ == '__main__':
    # load temp/test.wav using librosa
    y, sr = librosa.load('temp/test.wav', sr=44100)
    # convert to float32
    y = y.astype(np.float32)
    y = y[:44100]
    print(y.shape)

    result = vmlab_py.a2ev2_melspectrogram(y, 44100)

    mel = vmlab_py.RTMelV2(44100)
    mel.clear()

    # result2 = [] 
    # for i in range(0, 44100, 4410):
    #     retval = mel.transform(y[i:i + 4410])
    #     result2.extend(retval)
    #
    # # campare two result and result2
    # print(len(result))
    # print(len(result2))
    # print(type(result[0]))

    result2 = mel.transform(y)

    # both length will be greater than 19
    # so compare inside bytes. type inside result and result2 is bytes
    for i in range(len(result2)):
        if result[i] != result2[i]:
            print(f"result[{i}] != result2[{i}]")
            # print(f"result[{i}]: {result[i]}")
            # print(f"result2[{i}]: {result2[i]}")
            break
    else:
        print("All values are equal.")



