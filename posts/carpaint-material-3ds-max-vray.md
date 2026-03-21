# Creating a Car Paint Material with 3ds Max and VRay

**By Denis | October 08, 2017**

*Categories: Uncategorized*

*Thumbnail: https://i0.wp.com/dkcgi.net/wp-content/uploads/2017/10/Basic_Material.jpg?maxresdefault.jpg*

---

What is all this about ?

Well in short this post came to be as a direct request from one of the subscribers. Namely i was asked how to create a realistic car paint material. Initially i thought it would be a short and boring topic to cover it for a video. Needless to say i was wrong, so very wrong.
 Starting at the base

As soon as i started taking a better look into the car paint shader it started to get interesting. To get a realistic car paint shader you would need to approach this as it was in real life. If you have ever bothered to read about car paint, you will learn that it's a multple layer color.

[](https://i0.wp.com/www.dkcgi.net/wp-content/uploads/2017/10/D01.jpg)

In the image above you have a case where the paint of the car is getting damaged. This actually allows us to see that even though this is a metallic shader, the base is actually very glossy. This means that the first layer will control the color and doesn't need reflection. As soon as we get that done we can go over and create an additional layer for the coating. Once we have both of the layers created we can call it done or we can push on.

[](https://i1.wp.com/www.dkcgi.net/wp-content/uploads/2017/10/D02.jpg)

The next step was to create the flakes you see in the metallic color when it's sunny outside. To get this result i used Vray stochastic flakes material. This is a new addition to Vray since 3,6 . That means that if you want to get the same result as me you would need to have that version.  So if you want to see how i did the basic shader for the car paint material check out the video below.

{{youtube:VvcLzSQcSyQ}}

 

## Creating the Pearlescent color shader

After creating the basic shader i thought about pushing it a bit more and create a pearlescent version. That is basically a paint that changes color depending on the angle of viewing. You can see how that looks check out the image here.

[](https://i0.wp.com/www.dkcgi.net/wp-content/uploads/2017/10/PS03.jpg)

 

As you can see it looks cool and it's really not that hard to achieve. What i did was mix a different diffuse color base with a different mix curve and got the result. But since rarely are things in Max that simple you can see me doing it in the video below.

{{youtube:eK35RTvwxF0}}

So if you followed the two videos you now know how to create a basic and a pearlescent shader. And with that we put a end to today's topic. As always if you enjoyed it make sure you like the videos, comment and share. And don't forget to come back for more next time.