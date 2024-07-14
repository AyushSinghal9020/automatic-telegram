from flask import jsonify
import boto3
import os 

def upload_s3(file) : 

    s3 = boto3.client(
        's3' , 
        aws_access_key_id = 'AKIA6ODUZOOJMU43F36V' , 
        aws_secret_access_key = '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'
    )

    if file.filename == '' : return (
        jsonify({'error' : 'No file selected for uploading'}) , 
        400
    )

    if file and (file.filename.endswith('pdf') or file.filename.endswith('json')) : 

        file.save(f'Assets/uploads/main/{file.filename}')
        s3.upload_file(f'Assets/uploads/main/{file.filename}' , 'blubirch-pdf' , file.filename)

        os.remove(f'Assets/uploads/main/{file.filename}')
        return (
            jsonify({
                'message' : 'File successfully uploaded' ,
                'filename' : file.filename
            }) , 
            200
        )

    else : return (
        jsonify({'error' : 'Allowed file types are pdf or json'}) , 
        400
    )



def upload(file) : 

    if file.filename == '' : return (
        jsonify({'error' : 'No file selected for uploading'}) , 
        400
    )

    if file and (file.filename.endswith('pdf') or file.filename.endswith('json')) : 

        file.save(f'Assets/uploads/{file.filename}')
        
        return (
            jsonify({
                'message' : 'File successfully uploaded' ,
                'filename' : file.filename
            }) , 
            200
        )

    else : return (
        jsonify({'error' : 'Allowed file types are pdf or json'}) , 
        400
    )
