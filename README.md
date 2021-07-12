# Face Recognition System

The following codebase is a face recognition toolkit. It consists of three endpoints: A communal endpoint that uploads the images given an ID, an endpoint which copies these images to the image databaase, and an endpoints which verifies the image.

In this documentn we'll explain how this codebase works.

**Jump to Section**:
- [Face Recognition System](#face-recognition-system)
  - [Endpoints API](#endpoints-api)
    - [Resulting Codes](#resulting-codes)
  - [Run Development Mode](#run-development-mode)
    - [Environment Variables](#environment-variables)

## Endpoints API
After launching an instnce of `faceapp.py` on [development mode](#run-development-mode), you can use [Postman](https://www.postman.com/) or in case you're in mood for CLI, [cURL](https://curl.se/) to run the following commands. They, given the accopanying data, will trigger a chain of functions and they, in turn, will perform an action.

The following table documents these three endpoints:

|Endpoint|Method|Request Type|Response Type|Request Params|Response Params|
---------|------|------------|-------------|--------------|---------------|
`/upload_imgs?id=[id]`|POST|form-data|JSON|*files, id (arg)|upload_results, upload_code, upload_message, system_errors|
`/upload_db`|POST|x-www-form-urlencoded|JSON|upload_id, name, delete_pickles, rebuild_db, in_place|result_code, result_message, upload_results, system_errors|
`/verify`|POST|x-www-form-urlencoded|JSON|upload_id, skip_verify, skip_db_search, skip_liveness|recognition_code, recognition_message, recognition_results, system_errors|


Here's how it works.

You first upload how many images you want using `upload_imgs/?id=[reco_id]` for example `upload_imgs/?id=RECO_ID_000023`. The JSON response, if successful, will return the name of a subdirectory inside your UPLOAD_FOLDER (see: [Environment Variables](#environment-variables)). For example, `RECO_ID_000023-13134`.

`/upload_imgs` yields a JSON response which contain:

|Parameter|Yields|
|---------|------|
|upload_results|The result of the upload, containing scores, saved images, rejected images, and the `upload_id` which you have to give to the othre two endpoints.|
|upload_code|The resulting code. Refer to [codes](#resulting-codes) to get a sense of them.|
|upload_message|The message of the code.|
|system_errors|See [Environment Variables](#environment-variables)|


Now you have two options:

**Option 1**: Use `/upload_db` and save the faces inside the images, and a few augmented versions (depending on AUG_NUM, again see: [Environment Variables](#environment-variables)) to your DB_PATH under a subfolder called `{given_name}-{RECO_ID}`. The data wil lbe saved to MySQL.

The following form data can be passed to `upload_db`:

|Parameter|Job|
|---------|----|
delete_pickles|Delete all the .pkl files inside DB_PATH. Necessary if you wish for the **search model** (and not the verification) to recognize your images.|
rebuild_db|Rebuild the .pkl files. It's not necessary, because the datbase will be rebuilt upon the first search. However, for faster speed, it's better to enable it.|
in_place|Whether to replace the files, if the ID exists in the database, or add to them. If the ID doesn't exist in the database, and you enable it, it will inform you that this action was unnecessary.|
name|The name of the person in the photos.|
upload_id|The folder id that was given to you by `/upload_imgs`|

This endpoint will yield a JSON response containing the following keys:

|Parameter|Yields|
|---------|------|
|result_code|Refer to [codes](#resulting-codes)|
|result_message|The message of the code.|
|upload_results|Contains the results of the upload to images DB, such as the MySQL identifier, the resulting files, etc.|
|system_errors|See [Environment Variables](#environment-variables)|

After upload to image DB is done, the folder will be renamed and it can't be used anymore. 

**Option 2**: Use `/verify`, detect the faces, create augmented versions, and send the images down the verification pipline. 

`/verify` accepts the following keys:

|Parameter|Job|
|---------|---|
|upload_id|The folder id given to you by `/upload_imgs`. If this folder has been used for uploading to image DB, then it can't be used.|
|skip_verify|Skip verification, and just search the DB. Can be True or False.|
|skip_db_search|If verification doesn't yield results, don't search the DB. Can be either True or False. Between this and the last one, one, or either must be false. Both can't be true!|
|skip_liveness|Skip liveness detection.|

This endpoint will return the following results:

|Parameter|Yields|
|---------|---|
|recognition_code|Refer to [codes](#resulting-codes)|
|recognition_message|Resulting message.|
|recognition_results|Results, containing the name and the distance.|
|system_errors|See [Environment Variables](#environment-variables)|


### Resulting Codes
The API will return codes. These codes are stored in `codes_dict.py`. The `*_message` will return the message of this code. You can view the message for each code here:

|Code|Message|
|----|-------|
|176|There was problem with .env file on the server.|
|143|Both skip_verify and skip_db_search set to True.|
|153|At least one of the images doesn't exist. Consult log.|
|111|Length of img_paths is zero.|
|630|Could not detect a face in any of the images.|
|126|Regex matched ID.|
|127|Regex didn't match ID.|
|119|Files uploaded successfully.|
|117|Length of uploaded files was zero.|
|155|Database connection error. Consult log.|
|100|None of the matching IDs in the DB matched what was given.|
|134|After a search in the DB, the ID matched with what was found.|
|116|Problem getting ID, please check MySQL settings.|
|113|Path in the MySQL database doesn't exist in the image database.|
|200|Image successfully verified.|
|500|Image failed to verify and DB search was not enabled or was not a success.|
|150|Insert into MySQL failed. Please check your settings.|
|152|Failed to detect face in any of the images or all contained more than one face.|
|178|Problem loading liveness detection model. Check your URL.|
|560|All faces were spoof.|
|143|Both skip_verify and skip_db_search set to True. One must be False.|
|900|ID already exists in db and in_place was set to true. Folder deleted and DB path replaced.|
|838|ID successfully inserted into DB. in_place was needlessly enabled.|
|800|ID successfully inserted to db.|
|850|ID successfully inserted to db. in_place was disabled, so the files were added to the previous ones.|
|189|Folder already uploaded to DB. Can't verify to upload again. Or it does not exist at all!|
|107|Endpoint request needs to be www-form-urlencoded, or form is empty.|
|108|Acceptable upload_db endpoint www-form-urlencoded keys| upload_id, name, delete_pickles, rebuild_db, in_place.|
|109|Acceptable verify endpoint www-form-urlencoded keys| upload_id, skip_verify, skip_db_search, skip_liveness|
|110|No args provided for upload_imgs endpoint, or id arg must be provided through upload_imgs?id=|
|120|All the files were rejected due to not meeting score criteria.|

## Run Development Mode
For now, until I deploy this codebase to server and make a frontend for it, please test it by running it on your local machine. To do that:

1. Install Mini Conda.
2. Create an environment by `conda create -n face-reco python=3.9`
3. Activate the environment by `conda activate face-reco`
4. Navigate to the main folder and run `pip install -r requirements.txt`
5. Make sure the [Environment Variables](#environment-variables) are set and port 8001 is free.
6. Make sure MySQL is installed on your system and the schema and the table exist to what is specified in `.env`.
7. Run `python faceapp.py`.
8. Download Postman from the link earlier in this document.
9. Send requests.
10. If you run into any problems contact either me (`Chubak#7400`), Szymon, or Felix.
11. You may need to install dlib.

You can use [this file](https://drive.google.com/uc?id=1W9nSCmkPNr41MeDErwJuY_0rMKabsuak) to test. This file is also used in unit tests.


### Environment Variables
In order for this application to run, it requires a long list of environment variables. This file is validated, and if a key doesn't exist in it, or doesn't match the desired pattern, the endpoint will return `system_errors`. This key maps to two sub-keys, `not_in_env` which lists all the keys that are not in `.env` file, and `env_errs`, which contains all the errors generated from not matching the `.env` file. 

So create a file in the root called `.env` and make sure it contains the following keys, separted by a newline. Each key must be assigned with an equal sign (`KEY=VALUE`).

|Env Var Key|Description|Example|
|-----------|-----------|-------|
|MODEL_PATH|Path to the liveness model.|bin/model|
|MODEL_URL|URL to the liveness model on Google Drive. It should be the example|https://drive.google.com/uc?id=1G2RQ3rXtw6RmTjyBFlJEnd5UNo7zkRWX|
|MODEL_NAME|Name of your liveness model. Make sure you change it every time you change the model URL|liveness_best.h5|
|SQL_URI|URI of your MySQL installation.|localhost|
|SQL_USER|Your MySQL username.|root|
|SQL_PASS|Your MySQL password.|lasvegas|
|SQL_SCHEMA|Schema your MySQL table is in. Must exist.|world|
|SQL_TABLE|Your MySQL table. Must exist.|reco_table|
|ID_COL|Name of the Recognition ID column in the table. Must exist.|reco_id|
|PATH_COL|Name of the images path column in DB in the MySQL table. Must exist.|reco_path|
|NAME_COL|Name of the name column in MySQL table. Must exist.|reco_name|
|DB_PATH|Path to your images DB. Must exist.|I:\face_reco\db|
|TARGET_WIDTH|The width of the images in DB.|224|
|TARGET_HEIGHT|The height of the images in DB.|224|
|SELECTED_MODELS|Face recognition models you wish to use. Can be VGG-Face, Facenet, OpenFace, DeepFace, DeepID, ArcFace or Dlib.|Facenet,ArcFace,VGG-Face|
|ID_REGEX|The regex pattern for IDs.|RECO_ID_\d+|
|NUM_AUG|Number of augmentations.|4|
|SIM_FUNC|Distance function to use. Can be cosine, euclidean, or euclidean_l2|cosine|
|LOG_LOC|Location to the log file. Can be non-existent.|I:\face_reco\faceapp.log|
|VER_TOL|Real image verification tolerance. As in, how many real images need to be verified until the code returns true.|2|
|VER_TOL_AUG|Same as above, but for augmented images.|20|
|SUPER_PASSWORD|It's not in use yet. But needs to be there, and needs to be complex.|Spr!ngf!3ld_0h!0|
|SCORE_TOL|Minimum score acceoptable for uploaded images. Needs to be a decimal number.|7.000|
|UPLOAD_FOLDER|Uploaded images folder. Needs to exist.|I:\face_reco\static|


