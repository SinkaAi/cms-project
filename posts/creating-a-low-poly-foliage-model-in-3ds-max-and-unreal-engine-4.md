# Creating a Low Poly Foliage Model in 3ds Max and Unreal Engine 4

**By Denis | January 18, 2018**

*Categories: 3DS Max, Modeling, Unreal Engine*

*Thumbnail: https://i1.wp.com/dkcgi.net/wp-content/uploads/2018/01/Fern_UE4.jpg?maxresdefault.jpg*

---

The Idea

The idea for this post came from a simple need. That is the need to have a high quality, low poly foliage model. Main reason for this is that if we go in an import raw assets the poly count goes way up. Coming from a 3ds Max background, when needing to create grass and foliage i would use Forest Pack Pro. The main difference is that in Max you are rendering still image so having many instances is not an issue. Well the answer on how to get that quality into Real Time is what drove the idea for this post.

## Creating the Low Poly model

[](https://i1.wp.com/www.dkcgi.net/wp-content/uploads/2018/01/fern_felce_bush_20150405_1397521871.jpg)

When creating a low poly model, or any model for that matter Reference is king. This means that you always want to have an image of what you are creating at hand. We will try to create a fern model like the one above.

Creating something like that means that we will need a texture to start from. In general you can either take the pictures on your own, and prepare the textures. Or you can go over on Google and search for a texture with an Alpha map. Or alternative route would be to go to a site that sells textures like that. In my case i chose a texture from Megascans as those textures are high quality 4k images. You will see me set up the textures, then individually cut out all the leaves. After this i will show you how to get a controlling points with the help of bend modifiers. And in the end we will even see how to add vertex color.  The vertex color will later be used in UE4 for simulating wind. Knowing all this check out the video below to see how i did it.

{{youtube:ITtVita4QHQ}}

## Creating the UE4 Material

After creating the asset in 3ds Max we will jump over to UE4. Generally creating a material if you have all the nodes is a pretty easy procedure. You take all the nodes and plug them into the material and you're done. You will see me create a system for the Vertex Color that will control the wind. Another thing that i will show you is how to increase the normal map strength. And we will also see how to control the diffuse strength with the help of scalar parameters. Even though it's not that complex, some of the tricks there are pretty cool so check them out.

{{youtube:7qe6KXS4eY4}}

## Final Thoughts

Creating this post i have to admit was fun for me. Main reason is that i did a bit of research as well so i picked up some skills. I would like to say one thing to everyone out there, don't be scared of trying new stuff. I have received multiple messages of people telling me that UE4 looks too complex. Well honestly, it's really not that complex as long as you approach it with an open mind. Another driving force should be the fact that UE4 is going to be the main tool for Archviz. Maybe this will take some time but it will get there. So with this post i showed you the basics of creating foliage so you can use it in your scenes. I'll see that in the future i make more videos about modeling, and then using those models inside UE4.

Until then though, everyone stay safe and keep on learning.