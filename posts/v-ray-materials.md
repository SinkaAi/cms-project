# V-Ray Materials

**By Denis | September 21, 2015**

*Categories: 3DS Max, Starting With V-Ray, Vray*

*Thumbnail: https://i1.wp.com/dkcgi.net/wp-content/uploads/2015/09/V-Ray-Materials-Editor.jpg?maxresdefault.jpg*

---

Starting up with a new render engine can be a daunting task, especially if you worked with a different render engine for a while, Mental Ray or standard materials as an example. The main issue usually starts up when you don't know how to make heads or tails of the settings and the materials of the new render. Well in the [Starting With V-Ray series](http://www.dkcgi.net/category/vray/starting-with-v-ray-vray/) we went into depth on explaining the main settings for V-Ray and now in this post we will try to explain how the textures work in V-Ray. So brace yourselves as i think this is going to be a longer post, so lets just jump in right in the deep.

{{youtube:09w-Yk1Sok0}}

***I went ahead and made this into a video as well trying to explain the things that i went over in this post. I would highly recommend that if you want to understand how the materials in V-Ray work that you take some time and go over this post (WALL OF TEXT WITH PRETTY PICTURES) and hopefully clear up any things that aren't completely clear.** *

[](https://i0.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Material-Editor.jpg)

When you change your render from the default scanline render to V-Ray the one of the things that you will notice is that now your materials have been converted into V-Ray Materials (In order for this to be the default, you need to change it into the Customize – Custom UI and Defaults Switcher). The first thing that you are going to notice if you did it is that the material balls will be colored as you can see on the image here. This is a feature that V-Ray has implemented to make it easier to differentiate the materials, but if you ask me i would rather they kept it at the neutral gray, but then again it's my personal preference.

The main thing about V-Ray materials is that even though it looks and feels like it's complicated to deal with it, in reality V-Ray materials are basically created by tweaking three different parameters, Diffuse (main color), Reflection (self explanatory) and Refraction (the ability to let light pass through it)

Lets start from the beginning, namely how do we change the diffuse color of our material. That is quite simple and all you have to do is click on the color tab next to the diffuse (labeled 1).

Once you press the color tab you will get a color pallet looking like the one on the image shown below here. This color pallet is a fairly useful as it gives you a lot of leniency and flexibility when selecting the color that you need. We can separate it into a couple of different groups that would make it easier to explain it.

[](https://i1.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Material-Editor-03.jpg)

***The first type** of selection would be the selection by Hue in which you can select it my clicking anywhere in the selected field (marked with 2).

***The second thing** that you can control here is the brightness of the color you have selected (marked with 3)

***The third** is the RGB value selection. This here is a very helpful way of selecting as many times you would get a RGB value from a client for a color that he has in mind, and having a field where you can input the different values is of immense help (marked with 4)

***The fourth way** is a combined selection method where you visually choose from the Hue, Saturation and Value from the sliders shown with the field (marked 5)

So all this that we saw here so far is if we want to have a solid color for our diffuse, but in case we want to make a material that has an image or some pattern as a base then we have to add a bitmap, or a procedural map in the diffuse slot. The way to do this is you need to click on the little square next to the diffuse color picker and choose either a bitmap or a procedural map.

[](https://i0.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Diffuse.jpg)

On the image above we have a few different diffuse results. On the first one we have pure black color, that can be seen on the material ball on the left. Then the middle ball has a texture applied to it, and on the last one we have a procedural map where we can see the colors going from Red to White and Blue.

So what we need to understand here is that the Diffuse is the **MAIN Color** of our material.

The next in line is the **reflection slot**. As we mentioned earlier the reflection slot plays a big role in the final outcome of the look of our material so knowing how to control it is important. In order to get to the parameters to control the reflection you need to click on the color picker (marked on the image) and you will get the same color pallet as you saw in the diffuse section. Now here is where it starts to get interesting as the reflection is directly controlled by the **Whiteness** parameter. This means if the chosen color is black or a value of 0 you will have no reflection, while a white color or a value of 255 will mean a 100% reflective surface.

So to sum it up before we move onto examples, the percentage of 0-100% reflection is controlled by 255 segments in the Value color.

[](https://i1.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Reflection.jpg)

If we take a look at the image below we will see the reflection changes depending on the value we have selected. Going from left to right we can see how a 25% (64 value), 50% (128 value), 75% (192 value) and 100% (255 value) looks like when applied to a white material. (click for a larger size image)

[](https://i2.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Reflection-Scale.jpg)

While we are still at the reflection parameter we need to take a look at the **Reflection Glossiness** parameter as well. This parameter basically defines how blurry your reflections are going to be. The way to control the glossiness is through the numerical value of 0-1, where 1 is 100% shiny while 0 is 0% shiny. Now before you take this for granted i want to note one more thing, and that is that the majority of the materials you are going to be building will move from 0.5-0.99 range. There shouldn't be any reason to go below a range of 0.5 as with a 0.5 or 50% shiny reflections you will get some really blurry reflections, and you want to be weary of really blurry reflections as they love to gobble up rendering power and in turn ramp up your render times.

[](https://i1.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Reflection-Glosiness.jpg)

[](https://i0.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Reflection-Options.jpg)

While we are still at the Reflection we need to cover one more important thing, and that is the reflection color. When you are choosing the reflective intensity of your material you basically choose it from the Whiteness level of the color selector that goes in 255 increments of White-Gray-Black. Now in case you don't stick to the black and white gradient of the whiteness levels and choose to manually select a color in the reflection slot, in that case V-Ray won't simply make your Reflections stronger or weaker but in turn it will add coloring to the effect.

Now the reason why i mention this is because the way that colored reflections work is a bit tricky due to something called Energy preservation mode. By default this can be seen in the Material editor options roll down menu as shown on the image above, and the default setting is set at RGB. With an RGB Energy Preservation mode active the colored reflections that we choose for our materials will act weird in the sense that if you add red color in the reflection slot, instead of getting red reflections you will get reflections where the red color has been taken out of the reflection of the material.

If you look on the image below you can see exactly how that looks like. On the four examples below you can see a material with (Left to Right) Black, Blue, Green and Red. And no i didn't mix up the color places. The reason for the Blue color to appear Yellow, and the Blue to look Red and the Red to be Blue is due to the RGB energy preservation mode, because as you know all colors can be achieved with mixing Red, Green and Blue so once you take out one of those primary colors you get unexpected results.

[](https://i1.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Color-Reflection.jpg)

With this in mind it might sound like getting controllable colored reflections would be near impossible with V-Ray, but that is not the case. If you want to get reflections that are colored all you will need to do is switch the Energy preservation mode to Monochrome. In the image below you can see how a material with Monochrome reflections looks like. We have a Red, Green and Blue colors in the reflection slot and they are perfectly shown in the reflections as well.

[](https://i1.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Color-Reflection-Monochrome.jpg)

And the last thing that i would like to mention about the Reflection portion of the parameters is the **IOR (Index of Reflection)**. The IOR is basically the angle at which you are seeing reflections. In V-Ray 2.x versions the Fresnel Reflections (IOR) is turned off by default while in 3.x it's turned on. This IOR value actually has a pretty big impact on how our material is going to look like and the values range from 1 to basically infinite, but anything above 40 is hard to notice any difference. If you take a look at the image below you will see three examples of different reflections with different IOR values. So basically we have a IOR 1 and with that value we have no reflections as the angle is too steep for reflections to show up, then we come to a IOR 2 and we can see reflections forming up nice and realistic and in the last image we have IOR 6 value and a very reflective surface.

So to keep it simpler, with higher value for the IOR you will get more of the environment to reflect into your materials. If you want to get some realistic values for IOR's then simply Google the phrase "name of the materials you want" IOR value. [HERE IS AN EXAMPLE OF A SITE WITH ALOT OF IOR VALUES](http://www.pixelandpoly.com/ior.html).

[](https://i1.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Reflection-IOR.jpg)

So off to deal with **REFRACTION** now. Refraction is basically how much light can pass through a certain material, or simply put how transparent a material is really. The way to control the transparency is pretty much like with controlling the reflection with the Whiteness value. On the image here we can see how a material looks like with 0% Refraction, 50% Refraction and 100% Refraction

[](https://i1.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Refraction.jpg)

Now similar like with the reflection, we can use a color in the refraction slot, or we can even use a bitmap texture if we want. In the image below we can see the result that we get if we use a color, procedural texture (Gradient Falloff Red to Black) and a Bitmap texture in the last case (In retrospect i should have used a different color bitmap to make it different, but hey it's done so there)

[](https://i1.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Refraction-Colors.jpg)

So if we take a look at the images that we got with adding color in the refraction slot we can safely say that it ends up looking like colored glass. Well when you want to get colored glass this is not the wrong way, but it's not the right way either and let me explain why. V-Ray has the ability to portray colored glass much better then simply adding color in the refraction slot, it actually has a setting that is exactly for that purpose. This parameter is called **Fog Color**, and it can be found in the Refraction slot. 

If you take a look at the images below you will see that we have added a blue color to the Fog Color, and the strength of the effect is directly controlled by changing the For Multiplier. In the images below we have a multiplier od 10 then 1 then 0,1 and the last has 0.01. The main difference when using Fog Color is that depending on the thickness of the model that it was applied the effect will be stronger on thicker portions while it will be lighter on the thinner parts. This is that extra bit of realism that we get, as this is basically how light reacts in the real physical worlds. 

[](https://i2.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Fog-Color.jpg)

[](https://i0.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Refraction-Colors-Procedural.jpg)  If you click on the little square next to the Fog Color then we can choose to use a bitmap, or a procedural map that will help us control how the glass is going to look like. In my case i used a gradient map that goes from Red to Blue, and you can notice how in the middle where the model is the thinnest we can see the transition of the colors is best visible.

So with this option available to us we can see that we have a very good control on how the glass coloring is going to end up looking like in the end, and when working with materials the more control you have over all the parameters the better the end result is going to end up being. 

One thing that is worth mentioning here is that prior to 3.x version of V-Ray the option to add a map to control the fog color was not available, so in case you are using the 2.x version and can't find the option to add a bitmap know that the reason for that is that it doesn't come in your version of V-Ray. 

And before we finish with this now rather lengthy post, i want to go over one more option in the Refraction menu and that is the **Abbe option**. This option can be found under the IOR value for the Refraction (if you are using 3.x version) and by ticking the box next to Dispersion (if you are using 2.x version). What Abbe is controlling is basically the dispersion of light inside of the model. This is ideal for materials like crystals and diamonds, and to some extent some types of glass. If you take a look at the image below you will see three different values for Abbe, a Value of 1, 6 and 50 going left to right. We can notice that with a higher value, the dispersion of the light is more localized and it is giving us a more crystal appearance. 

[](https://i2.wp.com/www.dkcgi.net/wp-content/uploads/2015/09/V-Ray-Abbe.jpg)  

So with all of this that we went over here in this post we should have the basics of the Diffuse, Reflection and Refraction covered. Knowing these things is the first step towards knowing how to construct your basic materials, as well as more complex materials.