# Oxehealth-challenge

A repo to store information and progress around the Oxehealth platform engineer challenge

## Challenge 1

The first challenge is to write a program that will upload files from a local directory to an AWS S3 bucket. This is
expected to take no more than 4 hours.

Initial thoughts, and assumptions:

- The challenge says that this program should run on any variant of linux, but that you may also use any language of
  your choice. This is a point I would discuss further, however due to time constraints, I'm going to assume that
  means we can discount out of date linux variants, and just use python3.
- The program looks like the easiest part of this to write, with the meta-tooling and the testing structure being
  the most complicated/time-consuming piece. Given that I don't have a personal sandbox AWS account at the moment,
  that may end up taking as long as the script itself.
- I would ask further questions about the nature of the files being uploaded, and will make certain assumptions as
  follows:
    - Will any of the files be large? - I will be assuming no
    - How frequently will the files be uploaded/how often is the timer expecting to run (every minute, hourly etc.) -
      I will be assuming every 10 minutes
    - Related to the above, how often are new files generated? - I will be testing on a basis of a new file every minute
    - How large/clean is the destination S3 bucket? - I will be assuming that we cannot scan the bucket, to check if a
      file has already been uploaded. (I also believe that may be why we are deleting the files after upload)

### The Plan

From this I then plan to:

- Create an AWS account, and an S3 bucket
- Create a script that will generate these files, at random, approximately minutely intervals,
- Create the program that has actually been requested
- Using the tooling and credentials created earlier, verify that the program works as intended

### Progress

- Turns out I did have an AWS account lying around. Thank you password managers, and a bucket is trivial to create,
  so kathtestbucket now exists. Next step is to configure local environment access to the bucket. For this it is
  worth highlighting my developement machine is a mac, which I believe is Linux enough for the purposes of this, so
  won't be developing in docker.
- And a few moments later:

```
kat@Katherines-MacBook-Pro Repos % aws s3 ls
2023-08-12 10:16:34 kathtestbucket
```

### Progress 2

- I now have a script that will generate correctly shaped files, and have finished the testing framework, so I'm now
  ready to create the requested script.
- This script will now run in the background using tmux while I test and work from here.
- My initial thoughts are to use boto3, and I'll see how I get on!

### Progress 3

- The script is now written (upload-to-s3.py), though I'd remove the .py if I was using cron to automate it. The
  script is tested to work using manual local testing again my locally generated files and seems to be doing a good job.
- The script has not been configured to run automatically, or tested as part of systemd , but should have no issues
  being run in this way.
- My plan is to now polish the script, and consider final improvements that may be worth considering:
    - Handling different formats of directory (full paths vs relative paths, and how this effects uploaded names)
    - Handling files that are a part way through being written (as part of error handling)
    - Some unit testing, that would form part of the CI/CD pipeline, were I doing this in a production environment.

### progress 4

- From here I would write a test to ensure I don't upload/delete a file that is less than 30 seconds old, to match
  this requirement:

```
The files are being written by another process which is generating the data, and files
will usually be finished writing within a few seconds of the timestamp of the data
```

- I would write a CI test that runs the file creator once, then runs the upload service and ensures that the file is
  present in the bucket, and deleted locally. This test would be a requirement for any branch to merge going forwards.
- Finally, I would consider handling other formats of path (full vs relative).
- It is unclear if a crontab/systemd file is expected to be included in this project, however they are simple enough
  to add if required.

### Final requirements for part 1

- Each Linux machine would need to have local credentials, as suggested
- Each machine would need to have python installed, and present at the default location
- Each python installation would require boto3
- (This can be done with fewer requirements, however it didn't appear to need fewer requirements and is cleaner this
  way)

# Part 2

To turn this into a system critical service, I would start by making the above improvements, including designing
additional (automated) tests for the operating environment (e.g. ensuring that the systemd service file works
correctly), and I would make
them a requirement for any merge to main/deployment to production.

I would continue by:

- Integrating the logging with the existing logging infrastructure (especially instead of print statements)
- Utilise the existing monitoring infrastructure to ensure that the service is running correctly, and monitor for
  any critical errors

If there is no existing infrastructure, I would consider:

- Swapping the logging to use a logging service, such as datadog.
- Add a monitoring service, such as datadog, to each server to monitor the systemd service, and ensure it runs
  without errors, on schedule.
- This monitoring would report out to the 3rd party server, where we can have monitoring and alerting configured as
  necessary. It is not the only such service, but is one I have used in the past. (I would also consider cloudwatch
  for example.)
