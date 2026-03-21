# 3ds Max Modeling with Smoothing Groups

**By Denis | December 21, 2016**

*Categories: 3DS Max, Modeling*

*Thumbnail: https://i2.wp.com/dkcgi.net/wp-content/uploads/2016/12/Smoothing-Groups.jpg?maxresdefault.jpg*

---

Hey everyone and welcome to today's topic on 3ds max modeling, with the help of smoothing groups. First of all i want to note that this was initially a 2 part video. Upon finishing the original recording i actually saw that i was breaking an NDA that i had signed. NDA's are a pain, so i rerecorded the video to what you see here. But like all things everything has to have a start, so lets start from the beginning.
3ds Max Modeling with Smoothing Groups ?

You can do 3ds Max modeling with two different approaches. First is with chamfered edges approach to get the round look on edges. The second one is with the help of supporting geometry and turbosmooth modifier. They both have their advantages and disadvantages. So it would be great if we can combine the positives from the two workflows into one. This is where the modeling with smoothing groups comes into play.

## How do we combine them ?

Combining these two workflows is really not that hard as you will be able to see in the video below. The short explanation would be that we will use two different turbosmooth modifiers in one stack. The difference  is that the curvature of the faces will be controlled by the smoothing group.

[](https://i0.wp.com/www.dkcgi.net/wp-content/uploads/2016/12/smooth.png)If you have never worked with smoothing groups, you can change them by finding the menu. As you can see in the image here the smoothing groups look like a bunch of numbers in a calendar. The polygons that have the same smoothing group (SG) will try to make a smooth  surface. So if you have two or more polygons with the SG1 they will try to make a smooth surface. And if those polygons meet with other polygons with a different SG you will get a sharp edge. This right here is the base of the whole workflow of using smoothing groups for modeling.

## How does this help us ?

Understanding the SG concept is the base of working with this approach. The idea is that like i already said we will use two turbosmooth modifiers. The first one will control where the edges and curves will show up based on the SG. At same time the second one will control the sharpness of the edges. Now this is actually not that hard to grasp, and when explaining it it sounds a bit more complex. So instead of me trying to further explain how this works,  check out the video below and see for yourself.

{{youtube:M4Dw1abi30c}}

## Final Thoughts

If you watched the video and are back here reading this then kudos to you. As you might have seen it's a fairly powerful approach to modeling. The place where this shines is rapid prototyping modeling. So basically when you need to make your models very fast while they are still subject to changes. That means that this kind of modeling is more forgiving towards small issues and is very easy to modify. The down side is that it will give you a rather dense mesh. But at the same time Max has no problems with dealing with dense meshes if they are modifier stacks. The main issue is if you want to UV unwrap these models, in that case they can be a pain. So all in all it's a great way of modeling, and especially if you have to make high poly models.

So i hope you guys enjoyed this video, and you managed to learn something new today. That would be all for today, and as always if you enjoyed it help by sharing it around. Bye for now and i will see you next time.