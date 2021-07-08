# Face Recognition System

The following codebase is a face recognition toolkit. It consists of three endpoints: A communal endpoint that uploads the images given an ID, an endpoint which copies these images to the image databaase, and an endpoints which verifies the image.

In this documentn we'll explain how this codebase works.

* Jump to Section:
** [Endpoints](#endpoints-api)
** [Start on Development Mode](#run-development-mode)

## Endpoints API
After launching an instnce of `faceapp.py` on [development mode](#run-development-mode), you can use [Postman](https://www.postman.com/) or in case you're in mood for CLI, [cURL](https://curl.se/) to run the following commands. They, given the accopanying data, will trigger a chain of functions and they, in turn, will perform an action.

The following table documents these three endpoints:

|Endpoint|Method|Request Type|Response Type|Request Params|Response Params|
---------|------|------------|-------------|--------------|---------------|
`/upload_imgs?id=[id]`|POST|form-data|JSON|*files, id (arg)|upload_results, upload_code, upload_message, system_errors|
`/upload_db`|POST|x-www-form-urlencoded|JSON|upload_id, name, delete_pickles, rebuild_db, in_place|result_code, result_message, upload_results, system_errors|
`/verify`|POST|x-www-form-urlencoded|JSON|upload_id, skip_verify, skip_db_search, skip_liveness|recognition_code, recognition_message, recognition_results, system_errors|


Here's how it works.

1. You first upload how many images you want using `upload_imgs/?id=[reco_id]` for example `upload_imgs/?id=RECO_ID_000023`. The JSON response, if successful, will return the name of a subdirectory inside your UPLOAD_FOLDER (see: [Environment Variables](#environment-variables)). For example, `RECO_ID_000023-13134`.

Now you have two options:

**Option 1**: Use `/upload_db` and save the faces inside the images, and a few augmented versions (depending on AUG_NUM, again see: [Environment Variables](#environment-variables)) to your DB_PATH under a subfolder called `{given_name}-{RECO_ID}`. The data wil lbe saved to MySQL.

The following form data can be passed to `upload_db`:

|Parameter|Job"|
|---------|----|
delete_pickles| Delete all the .pkl files inside DB_PATH. Necessary if you wish for the **search model** (and not the verification) to recognize your images.
rebuild_db| Rebuild the .pkl files. It's no necessary, because the datbase will be rebuilt upon the first search.



**Option 2**: Use `/verify`, detect the faces, create augmented versions, and send the images down the verification pipline. 