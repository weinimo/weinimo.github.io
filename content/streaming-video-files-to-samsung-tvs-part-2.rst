Streaming video files to Samsung TVs (Part 2)
#############################################
:date: 2012-06-15 20:49
:author: Thomas Weininger
:category: Free Software
:tags: DLNA, Linux, Ruby, Samsung TV
:slug: streaming-video-files-to-samsung-tvs-part-2

The second (and final) part of my article series about streaming video
files to Samsung TVs describes which video and audio codecs as well as
which container formats to choose for playing back video files on
Samsung devices (tested with UE40D6200). Furthermore I'll show you a
Ruby program I wrote for transcoding files automatically to the right
format.

I have many files like Flash video files from YouTube, recorded MPEG2
transport streams from my PVR and other media files my TV doesn't
understand or doesn't support very well. Unfortunately, many of them
must be transcoded to another format which is more suitable for the TVs
DLNA function. To find the best formats for the conversation I've
started a series of tests. I took a video file and transcoded it using
many different video and audio codecs and container formats and checked
their compatibility with Samsungs SmartHub. To keep this article short,
I show you only the summary of my tests instead of the full results. In
short that is:

Video codecs that don't need to be converted:

-  H264
-  MPEG4
-  WMV3

Audio codecs that don't need to be converted:

-  MP3
-  AAC
-  AC3

My investigation showed that both the Matroska (.mkv) and the MPEG4
(.mp4) container formats are most suiteable for my scenario.

Above stated rules are simplified as there are also other constraints to
consider when trying to make ones video collection ready for streaming.
I wrote a sweet little Ruby program that is much more sophisticated and
takes care of most codecs and handles them the right way automatically.
It scans given paths or single video files and converts them if
necessary. One goal while designing the tool was to keep the original
quality of the files whenever possible. To achieve this it handles the
audio and video stream of the file independently from each other and
transcodes only those parts that need to be converted. So for instance
if the video stream needs to be converted, but the audio stream does
not, it only changes the video stream and takes the audio track from the
original file.

My program depends on FFMPEG and the Ruby package `streamio-ffmpeg`_.
You can install it using gem via:

.. code:: text

    (sudo) gem install streamio-ffmpeg

It's also important that your FFMPEG installation supports libfaac
encoding. To check this simply type "ffmpeg" in your terminal. If there
is a line "libfaac" with an "E" in one of the columns before the codec
name, then everything is fine.

I think the code is pretty selfexplaining. It's far from perfect, but in
practice it works very well. Usage is simple:

.. code:: text

    ffautoconv.rb <file(s)/path(s) to scan>

It writes a logfile to /tmp/ffautoconv.log while running so it's
possible to reconstruct what the program was doing.

Please leave a comment if you have a suggestion or simply found my
program useful. Here's the download link: `ffautoconv`_.

.. code:: ruby

    #!/usr/bin/env ruby
    # ffautoconv.rb: Program for transcoding videos for streaming them to Samsung TVs.
    # Author: Thomas Weininger (http://blog.weinimo.de)
    # This program is free software: you can redistribute it and/or modify it under the terms of the BSD license.

    require 'find'
    require 'rubygems'
    require 'streamio-ffmpeg'

    def containerChange (movie, filename, container)
      if File.extname(filename) != "." + container
        $logfile.write("New container of  #{filename} will be: #{container}.
         \n  Original file: #{movie.video_codec}, acodec: #{movie.audio_codec}\n")
        newfilename = filename.chomp(File.extname(filename)) + ".#{container}"
        movie.transcode(newfilename, "-vcodec copy -acodec copy -copyts")

        # Check whether container change was successful.
        newmovie = FFMPEG::Movie.new(newfilename)
        if newmovie.valid?
          $logfile.write("  Container format changed successfully. Deleting " + filename + ".\n\n")
          File.delete(filename)
        else
          $logfile.write("  Error occured while trying to change the container format. Deleting " + newfilename + ".\n\n")
          File.delete(newfilename)
        end
      else
        $logfile.write("Container of " + filename + " doesn't have to be changed" +
          ".\n  Original file: #{movie.video_codec}, acodec: #{movie.audio_codec}.\n\n")
      end
    end

    def reencode (movie, filename, acodec, vcodec, container)
      # Decide whether we need to transcode or only a container change.
      if movie.audio_codec.nil?                                                     # Prevent NoMethodError if no audio track is available.
        orig_acodec = ""
      else
        orig_acodec = movie.audio_codec
      end

      if ( ( orig_acodec.match(/^#{acodec}(.*)/) && movie.video_codec.match(/^#{vcodec}(.*)/) ) ||
           ( acodec == "copy" && vcodec == "copy" ) )
        containerChange(movie, filename, container)
      else
        $logfile.write("New Codecs of #{filename} will be: #{vcodec}, #{acodec}, #{container}.\n" +
          "  Original file: #{movie.video_codec}, acodec: #{movie.audio_codec}.\n")
        $logfile.flush
        newfilename = filename.chomp(File.extname(filename)) + ".#{container}"
        options = { :threads => 0 }
        customopts = ""

        if ( movie.video_codec.match(/^#{vcodec}(.*)/) || vcodec == "copy" )        # Can we use the video track from the original file?
          customopts = "#{customopts} -copyts"
          options = options.merge({ :video_codec => "copy", :custom => customopts })
        else
          case vcodec
          when "h264"
            customopts = "#{customopts} -qscale 0"
            options = options.merge({ :video_codec => "libx264", :custom => customopts })
          end
        end

        if ( orig_acodec.match(/^#{acodec}(.*)/) || acodec == "copy" )        # Can we use the audio track from the original file?
          options = options.merge({ :audio_codec => "copy" })
        else
          case acodec
          when "aac"
            customopts = "#{customopts} -aq 120"
            options = options.merge({ :audio_codec => "libfaac", :custom => customopts })
          end
        end

        begin
          puts "\nTranscoding: #{filename}.\n"
          beginning_time = Time.now
          movie.transcode(newfilename, options) { |progress| print "\r#{Integer(progress*100)}%" }
          total_secs = Time.now - beginning_time
          combined_mins = (total_secs / 60).floor
          combined_secs = (total_secs % 60).floor
          $logfile.write("  Time elapsed: #{combined_mins} minutes, #{combined_secs} seconds (#{total_secs} seconds).\n")
        rescue RuntimeError => e
          $logfile.write("  RUNTIME ERROR occured!!!\n\n")
          return
        rescue Interrupt => e
          puts "SIGINT caught. Deleting #{newfilename} and exiting after that."
          File.delete(newfilename)
          exit
        end

        # Check whether transcoding was successful.
        newmovie = FFMPEG::Movie.new(newfilename)
        if newmovie.valid?
          $logfile.write("  Transcoding completed successfully. Deleting " + filename + ".\n\n")
          File.delete(filename)
        else
          $logfile.write("  Error occured while transcoding. Deleting " + newfilename + ".\n\n")
          File.delete(newfilename)
        end
      end
    end

    $logfile = File.open("/tmp/ffautoconv.log", File::WRONLY|File::TRUNC|File::CREAT|File::APPEND)
    FFMPEG::logger.level = Logger::WARN

    ARGV.each do |a|
      Find.find(a) do |f|
        movie = FFMPEG::Movie.new(f)
        if movie.valid?
          dstACodec = "copy"                                                        # Always use the old audio track.

          # Decide new video codec depending on the video codec of the original file.
          case movie.video_codec
          when /^h264(.*)/, /^mpeg4(.*)/, /^wmv3(.*)/                               # Video codecs that don't need to be transcoded.
            dstVCodec = "copy"
          when /^flv(.*)/, /^vp6f(.*)/, /^msmpeg4(.*)/, /^theora(.*)/,
               /^wmv1(.*)/, /^wmv2(.*)/, /^vc1(.*)/, /^rv40(.*)/                    # Video codecs that need to be transcoded.
            dstVCodec = "h264"
          when /^mpeg2video(.*)/, /^mpeg1video(.*)/                                 # MPEG videos need special treatment.
          when /^mjpeg(.*)/
            next
          else
            $logfile.write("#{f}: vcodec not handled: #{movie.video_codec}, acodec: #{movie.audio_codec}\n\n")
            next
          end

          # Decide which container format we should take depending on the audio codec of the original file.
          case movie.audio_codec
          when nil?, /aac(.*)/, /mp3(.*)/, /ac3(.*)/                                # ffmpeg mp4 does NOT support WMA, but wmv does. See http://en.wikipedia.org/wiki/Comparison_of_container_formats
            dstACodec = "aac" if movie.video_codec =~ /^vp6f(.*)/
            # Change container for audio formats that are supported by the mp4 container.
            dstContainer ||= "mp4"
          when /cook(.*)/
            dstACodec = "aac"
            dstContainer ||= "mp4"
          else # wmav2, sipr
            # Matroska offers the best format support for all possible audio codecs.
            dstContainer ||= "mkv"
          end

          reencode(movie, f, dstACodec, dstVCodec, dstContainer)
          $logfile.flush
        end
      end
    end
    $logfile.close

 

.. _streamio-ffmpeg: https://github.com/streamio/streamio-ffmpeg
.. _ffautoconv: http://weininger.net/wp-content/uploads/2012/06/ffautoconv.gz
