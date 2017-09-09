# Text mining to uncover complex incident types

There are three main reasons for the decline in the number of fires in London since the 1980s. First, technologies have improved including fire retardant materials, smoke detectors, and sprinkler systems. Second, the London Fire Brigade’s (LFBs) active education and outreach programme has been very effective at raising awareness of fire safety issues. Finally, data has been methodically collected and used by the LFB to discover patterns, which has been key to identifying fire risk, leading to informed policy and decision making.



The LFB collect a lot of data; each incident attended is recorded in a data set with 76 multiple choice  fields, including information about the time, location, and ignition source of a fire. The business intelligence unit at LFB do a fantastic job of analysing these data. In addition to this large categorical dataset Fire Investigators also write free text reports for more serious incidents. Since the year 2000 the LFB have amassed an archive of over 37,000 free text reports. This data gold mine has taken hundreds of hours to write, yet historical reports have been sitting dormant because it is difficult to quickly extract information from this volume of free text. If a human were to attempt to interpret this it would take 40 days, and 40 nights just to read it.

Within Natural Language processing topic modelling is useful to discover abstract categories. We can explain topic modelling using the analogy of a library. As humans we intuitively cluster books into genres, such as sci-fi, crime or romance books. The librarian works to sort new books into the appropriate category. But what if we gave the librarian 100,000 books without any titles or prior knowledge of genres?

As it turns out computers excel at this kind of task. A computer can take a collection of documents, apply a model to look at the distribution of words in each document. Then find similarities between documents, and group these similar documents into topics/genres.

To identify topics that describe fire scenarios within the collection of 37,000 fire reports I used a topic modelling approach called Latent Dirichlet Allocation. Here are some example topics that were discovered using by the algorithm:

The topics extracted are fairly intuitive describing fires involving for example unattended candles, the disposal of cigarettes, or electrical faults. The most common topic found describes fires in dwellings, with words such as smoke, flat, and floor. A very interesting and potentially more complex topic that this method discovered was fires involving an accumulation of grease, fat, and oil in restaurant extraction and ducting systems. In this data we found approximately 300 of these ducting fires.

Using this topic modelling approach along with the other categorical data collected by the LFB we can explore different topics in more detail. If we take the example of ducting fires. We can see in recent years there has been a significant increase in the number of ducting fires, despite the general decrease in fires in London.

This approach also allows us to explore more subtle fire types that may not be well recorded by the structured data set. I created a tool to explore the geographic distribution of topics, again using the example of the ducting fires,. In the below image each red circle represents a ducting fire, where the circle radius indicates the fire severity, larger circles are larger fires. Individual data points can also be viewed by clicking on the circle. We can see that this ducting problem is particularly dangerous in areas like Soho and along Edgware road. This information could potentially be used to provide more targeted maintenance and fire inspection visits in these areas.

For the first time we have given the LFB the tools to analyse these free text reports. These new tools along with the existing expertise at the LFB will help to effectively use the available data to make more informed decisions, guide policy, and thereby help to reduce fire deaths in London even further.
