��    m      �  �   �      @	  &   A	  �  h	  �   .  v  �  �   I  $  �  o            �     �     �     �     	  -        E  %   `     �     �     �  	   �     �  !   �     	          ,  1   @  +   r     �  f   �  8     H   O  +   �     �  >   �          #     6     >     Z     u  5   |  0   �     �             '   ?     g  $   �     �     �  2   �  #        A  f   R     �  >   �  
     2     +   F     r     �     �     �     �     �  8   �            .  )   O  +   y      �  -   �      �  4        J     a     z  )   �     �  l   �     G     d     }     �  "   �  S   �     *     6     <  C   P     �  .   �  $   �        $   #  $   H     m     |     �  0   �     �     �  %        2     C  6   U     �  3   �  �  �  &   �  �  �  �   �!  v  P"  �   �#  $  h$  o  �%     �&     '     4'     N'     j'     �'  -   �'     �'  %   �'     (     "(     ;(  	   C(     M(  !   e(     �(     �(     �(  1   �(  +   �(     )  f   -)  8   �)  H   �)  +   *     B*  >   T*     �*     �*     �*     �*     �*     �*  5   �*  0   0+     a+     +     �+  '   �+     �+  $   ,     ),     H,  2   h,  #   �,     �,  f   �,     7-  >   G-  
   �-  2   �-  +   �-     �-     	.     .     '.     B.     F.  8   R.      �.      �.  )   �.  +   �.      #/  -   D/      r/  4   �/     �/     �/     �/  )   0     @0  l   X0     �0     �0     �0     1  "   11  S   T1     �1     �1     �1  C   �1     2  .   ,2  $   [2      �2  $   �2  $   �2     �2     �2     3  0   53     f3     x3  %   �3     �3     �3  6   �3     
4  3   !4     %   X                   3   =           U          M   ;       9       l                 H   4      >          1       -       [      $   5              S      R   D   i   !   a       6   \   ,       E           k   &       .          +   `   A   "   	      b       Y       0   ?   (               Q       G   :            j   N             W       K   T   @   g      )         h       I          B       c   8   C   d         <         J   2   m   *              #   e   Z           ^           ]   7      '   
   O   F   V      _   P   L                 f   /    
  The current value for my_style is:  
'normal' will attempt to display the sites the same ways as 'trusted' does
except that it will remove any styling deemed suspicious (see the docs for
details) and will validate any image source before allowing the image to
be displayed.  If the site contains many images, this validation process
will slow down the display.  Images that can not be validated will not be
shown.  Each image is validated only once during a given Crunchy session.
         
'strict' will remove all styling and image on the page.  It will result
in the fastest display, but one that will likely be the least visually
appealing.
         
'trusted' should only be used for sites that you are convinced will
not attempt to insert malicious code.  Sites that allow users to post
comments, or worse, that allow users to edit (such as wikis) should not
be set to 'trusted'. With 'trusted' selected, Crunchy will display the
site as closely as it can to the wayt the original looked using only
 your browser.
         
Crunchy will remove any pre-existing javascript code on the page as
well as a number of html elements that could be used to hide some
javascript code.
         
Selection of a 'display MODE' will result in the same processing by Crunchy
as the selection of 'MODE' except that no interactive elements
(such as a Python interpreter)
will be inserted in the page, thereby preserving the normal browser
sandbox to protect your computer from malicious code. 
You can change some of the default values by Crunchy, just like
you can obtain this help message, using either an interpreter
prompt or an editor, and assigning the desired value to a given
variable.  Some of these variables are "fixed", which means that
their value can not be changed by the user.
-
Here are the values of some variables currently used by Crunchy.
   The current value is:   %d elements were removed. -   Crunchy security level:   No elements were removed.   One element was removed. -   View report   by the user's choice specified in %s.styles
 # no code entered by user
 (Fixed) Temporary working directory:  (Fixed) User home directory:  An exception was raised: Approve Attribute Attribute (if relevant) Before browsing any further ...

 Cancel Confirm the security levels Confirmation code:  Congratulations, your code passed all (%d) tests! Congratulations, your code passed the test! Copy code sample Crunchy could not open the page you requested. This could be for one of anumber of reasons, including: Crunchy will attempt to provide friendly error messages. Crunchy's error messages will be similar to Python's default tracebacks. Crunchy: could not style the following code Directory Listing Do you wish to retain the existing settings for these sites?

 Error on line Error on line %s:
 Execute Execute as external program Execute as separate thread Host:  If set to True, Crunchy's default styles are replaced If you want to preserve the existing selection,  Illegal path, page not found. Invalid choice for %s.dir_help Invalid choice for %s.doc_help Invalid choice for %s.editarea_language Invalid choice for %s.language Invalid choice for %s.local_security Invalid choice for %s.my_style Invalid choice for %s.no_markup Invalid choice for %s.override_default_interpreter Invalid choice for %s.site_security Load Python file Note: while this is a valid choice, this choice is not available for a language provided by editarea.  Number of times Parsing error occurred in the following Python code.
Info: %s. Remove all Removed: attribute, or attribute value not allowed Removed: style tag or attribute not allowed Removed: tag not allowed Save Python file Save and Run Select site security level Tag Tag removed The choices for "pre" tag without Crunchy markup are %s
 The choices for dir_help are %s
 The choices for doc_help are %s
 The choices for editarea_language are %s
 The choices for friendly tracebacks are %s
 The choices for language are %s
 The choices for local_security levels are %s
 The choices for my_style are %s
 The choices for override_default_interpreter are %s
 The current value is:  The expected result was: The following example failed: The language choice for editarea remains  The page doesn't exist. The path you requested was illegal, examples of illegal paths include those containing the .. path modifier. The path you requested was:  The result obtained was: The valid choices are:  There was no test to satisfy. Type %s.help for more information. Use 'Save and Run' to execute programs (like pygame and GUI based ones) externally. User's code Value Value (if relevant) You can change any of them before clicking on the approve button.

 You code failed the test. You may select a site specific security level: Your code failed %s out of %s tests. Your code failed all (%d) tests. Your program tried to exit Crunchy.
 builtins not defined in console yet. called by line editarea_language also set to:  editarea_language set to:  friendly attribute must be set to True or False. language set to:  my_style set to:  override_default_interpreter set to:  remove from list security set to:  simply dismiss this window by clicking on the X above. site security set to:  with "image_file   file_name" as a required option. Project-Id-Version: rur-ple
POT-Creation-Date: 
PO-Revision-Date: 2007-08-23 21:21-0400
Last-Translator: André Roberge <andre.roberge@gmail.com>
Language-Team:  <andre.roberge@gmail.com>
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
X-Poedit-Language: English
X-Poedit-Basepath: C:\documents and settings\André\my documents\crunchy\branches\andre
X-Poedit-SearchPath-0: ..\andre
X-Poedit-SearchPath-1: src
X-Poedit-SearchPath-2: src\plugins
 
  The current value for my_style is:  
'normal' will attempt to display the sites the same ways as 'trusted' does
except that it will remove any styling deemed suspicious (see the docs for
details) and will validate any image source before allowing the image to
be displayed.  If the site contains many images, this validation process
will slow down the display.  Images that can not be validated will not be
shown.  Each image is validated only once during a given Crunchy session.
         
'strict' will remove all styling and image on the page.  It will result
in the fastest display, but one that will likely be the least visually
appealing.
         
'trusted' should only be used for sites that you are convinced will
not attempt to insert malicious code.  Sites that allow users to post
comments, or worse, that allow users to edit (such as wikis) should not
be set to 'trusted'. With 'trusted' selected, Crunchy will display the
site as closely as it can to the wayt the original looked using only
 your browser.
         
Crunchy will remove any pre-existing javascript code on the page as
well as a number of html elements that could be used to hide some
javascript code.
         
Selection of a 'display MODE' will result in the same processing by Crunchy
as the selection of 'MODE' except that no interactive elements
(such as a Python interpreter)
will be inserted in the page, thereby preserving the normal browser
sandbox to protect your computer from malicious code. 
You can change some of the default values by Crunchy, just like
you can obtain this help message, using either an interpreter
prompt or an editor, and assigning the desired value to a given
variable.  Some of these variables are "fixed", which means that
their value can not be changed by the user.
-
Here are the values of some variables currently used by Crunchy.
   The current value is:   %d elements were removed. -   Crunchy security level:   No elements were removed.   One element was removed. -   View report   by the user's choice specified in %s.styles
 # no code entered by user
 (Fixed) Temporary working directory:  (Fixed) User home directory:  An exception was raised: Approve Attribute Attribute (if relevant) Before browsing any further ...

 Cancel Confirm the security levels Confirmation code:  Congratulations, your code passed all (%d) tests! Congratulations, your code passed the test! Copy code sample Crunchy could not open the page you requested. This could be for one of anumber of reasons, including: Crunchy will attempt to provide friendly error messages. Crunchy's error messages will be similar to Python's default tracebacks. Crunchy: could not style the following code Directory Listing Do you wish to retain the existing settings for these sites?

 Error on line Error on line %s:
 Execute Execute as external program Execute as separate thread Host:  If set to True, Crunchy's default styles are replaced If you want to preserve the existing selection,  Illegal path, page not found. Invalid choice for %s.dir_help Invalid choice for %s.doc_help Invalid choice for %s.editarea_language Invalid choice for %s.language Invalid choice for %s.local_security Invalid choice for %s.my_style Invalid choice for %s.no_markup Invalid choice for %s.override_default_interpreter Invalid choice for %s.site_security Load Python file Note: while this is a valid choice, this choice is not available for a language provided by editarea.  Number of times Parsing error occurred in the following Python code.
Info: %s. Remove all Removed: attribute, or attribute value not allowed Removed: style tag or attribute not allowed Removed: tag not allowed Save Python file Save and Run Select site security level Tag Tag removed The choices for "pre" tag without Crunchy markup are %s
 The choices for dir_help are %s
 The choices for doc_help are %s
 The choices for editarea_language are %s
 The choices for friendly tracebacks are %s
 The choices for language are %s
 The choices for local_security levels are %s
 The choices for my_style are %s
 The choices for override_default_interpreter are %s
 The current value is:  The expected result was: The following example failed: The language choice for editarea remains  The page doesn't exist. The path you requested was illegal, examples of illegal paths include those containing the .. path modifier. The path you requested was:  The result obtained was: The valid choices are:  There was no test to satisfy. Type %s.help for more information. Use 'Save and Run' to execute programs (like pygame and GUI based ones) externally. User's code Value Value (if relevant) You can change any of them before clicking on the approve button.

 You code failed the test. You may select a site specific security level: Your code failed %s out of %s tests. Your code failed all (%d) tests. Your program tried to exit Crunchy.
 builtins not defined in console yet. called by line editarea_language also set to:  editarea_language set to:  friendly attribute must be set to True or False. language set to:  my_style set to:  override_default_interpreter set to:  remove from list security set to:  simply dismiss this window by clicking on the X above. site security set to:  with "image_file   file_name" as a required option. 